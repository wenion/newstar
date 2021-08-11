from datetime import datetime, timedelta

import pytest
from h_matchers import Any

from h import models
from h.security import Identity
from h.services.auth_ticket import (
    TICKET_REFRESH_INTERVAL,
    TICKET_TTL,
    AuthTicketNotLoadedError,
    AuthTicketService,
    auth_ticket_service_factory,
)


class TestAuthTicketService:
    def test_userid_raises_when_ticket_has_not_been_loaded_yet(self, svc):
        with pytest.raises(AuthTicketNotLoadedError) as exc:
            svc.userid()
        assert str(exc.value) == "auth ticket is not loaded yet"

    def test_userid_returns_the_users_userid(self, svc, ticket):
        svc.usersvc.fetch.return_value = ticket.user

        svc.verify_ticket(ticket.user_userid, ticket.id)

        userid = svc.userid()
        assert ticket.user.userid == userid

    def test_groups(self, svc, ticket, principals_for_identity):
        svc.verify_ticket(ticket.user_userid, ticket.id)

        result = svc.groups()

        svc.usersvc.fetch.assert_called_once_with(ticket.user_userid)
        principals_for_identity.assert_called_once_with(
            Any.instance_of(Identity).with_attrs(
                {"user": svc.usersvc.fetch.return_value}
            )
        )
        assert result == principals_for_identity.return_value

    def test_groups_raises_when_ticket_is_not_loaded(self, svc, ticket):
        with pytest.raises(AuthTicketNotLoadedError) as exc:
            svc.groups()
        assert str(exc.value) == "auth ticket is not loaded yet"

    def test_verify_ticket_fails_when_id_is_None(self, svc):
        assert not svc.verify_ticket(self.principal, None)

    def test_verify_ticket_fails_when_id_is_empty(self, svc):
        assert not svc.verify_ticket(self.principal, "")

    @pytest.mark.usefixtures("ticket")
    def test_verify_ticket_fails_when_ticket_cannot_be_found(self, svc, db_session):
        assert not svc.verify_ticket("foobar", "bogus")

    def test_verify_ticket_fails_when_ticket_user_does_not_match_principal(
        self, svc, db_session, ticket
    ):
        assert not svc.verify_ticket("foobar", ticket.id)

    def test_verify_ticket_fails_when_ticket_is_expired(
        self, svc, db_session, factories
    ):
        expires = datetime.utcnow() - timedelta(hours=3)
        ticket = factories.AuthTicket(expires=expires)
        db_session.flush()

        assert not svc.verify_ticket(ticket.user_userid, ticket.id)

    def test_verify_ticket_succeeds_when_ticket_is_valid(self, svc, db_session, ticket):
        assert svc.verify_ticket(ticket.user_userid, ticket.id) is True

    def test_verify_ticket_skips_extending_expiration_when_within_refresh_interval(
        self, svc, db_session, factories
    ):
        ticket = factories.AuthTicket(updated=datetime.utcnow())
        db_session.flush()

        expires_before = ticket.expires

        svc.verify_ticket(ticket.user_userid, ticket.id)
        db_session.flush()

        # Manually expire ticket, so that the data will be reloaded from the
        # database.
        db_session.expire(ticket)
        assert expires_before == ticket.expires

    def test_verify_ticket_extends_expiration_when_over_refresh_interval(
        self, svc, db_session, factories
    ):
        ticket = factories.AuthTicket(
            updated=(datetime.utcnow() - TICKET_REFRESH_INTERVAL)
        )
        db_session.flush()

        expires_before = ticket.expires

        svc.verify_ticket(ticket.user_userid, ticket.id)
        db_session.flush()

        # Manually expire ticket, so that the data will be reloaded from the
        # database.
        db_session.expire(ticket)
        assert expires_before < ticket.expires

    def test_add_ticket_raises_when_user_cannot_be_found(self, svc):
        svc.usersvc.fetch.return_value = None

        with pytest.raises(ValueError) as exc:
            svc.add_ticket("bogus", "foobar")

        assert str(exc.value) == "Cannot find user with userid bogus"

    def test_add_ticket_stores_ticket(self, svc, db_session, user, utcnow):
        svc.usersvc.fetch.return_value = user

        utcnow.return_value = datetime(2016, 1, 1, 5, 23, 54)

        svc.add_ticket(user.userid, "the-ticket-id")

        ticket = db_session.query(models.AuthTicket).first()
        assert ticket.id == "the-ticket-id"
        assert ticket.user == user
        assert ticket.user_userid == user.userid
        assert ticket.expires == utcnow.return_value + TICKET_TTL

    def test_add_ticket_caches_the_userid(self, svc, db_session, user):
        svc.usersvc.fetch.return_value = user

        assert svc._userid is None
        svc.add_ticket(user.userid, "the-ticket-id")
        assert svc._userid == user.userid

    @pytest.mark.usefixtures("ticket")
    def test_remove_ticket_skips_deleting_when_id_is_None(self, svc, db_session):
        assert db_session.query(models.AuthTicket).count() == 1
        svc.remove_ticket(None)
        assert db_session.query(models.AuthTicket).count() == 1

    @pytest.mark.usefixtures("ticket")
    def test_remove_ticket_skips_deleting_when_id_is_empty(self, svc, db_session):
        assert db_session.query(models.AuthTicket).count() == 1
        svc.remove_ticket("")
        assert db_session.query(models.AuthTicket).count() == 1

    def test_remove_ticket_deletes_ticket(self, svc, ticket, factories, db_session):
        keep = factories.AuthTicket()

        assert db_session.query(models.AuthTicket).count() == 2
        svc.remove_ticket(ticket.id)
        assert db_session.query(models.AuthTicket).get(keep.id) is not None
        assert db_session.query(models.AuthTicket).get(ticket.id) is None

    def test_remove_ticket_clears_userid_cache(self, svc, ticket):
        svc.verify_ticket(ticket.user_userid, ticket.id)

        assert svc._userid is not None
        svc.remove_ticket(ticket.id)
        assert svc._userid is None

    @property
    def principal(self):
        return "acct:bob@example.org"

    @property
    def ticket_id(self):
        return "test-ticket-id"

    @pytest.fixture
    def svc(self, db_session, user_service):
        return AuthTicketService(db_session, user_service)

    @pytest.fixture
    def principals_for_identity(self, patch):
        return patch("h.services.auth_ticket.principals_for_identity")

    @pytest.fixture
    def ticket(self, factories, user, db_session):
        ticket = factories.AuthTicket(user=user, user_userid=user.userid)
        db_session.flush()
        return ticket

    @pytest.fixture
    def user(self, factories, db_session):
        user = factories.User()
        db_session.flush()
        return user


@pytest.mark.usefixtures("user_service")
class TestAuthTicketServiceFactory:
    def test_it_returns_auth_ticket_service(self, pyramid_request):
        svc = auth_ticket_service_factory(None, pyramid_request)
        assert isinstance(svc, AuthTicketService)

    def test_it_provides_request_db_as_session(self, pyramid_request):
        svc = auth_ticket_service_factory(None, pyramid_request)
        assert svc.session == pyramid_request.db

    def test_it_provides_user_service(self, pyramid_request, user_service):
        svc = auth_ticket_service_factory(None, pyramid_request)
        assert svc.usersvc == user_service


@pytest.fixture
def utcnow(patch):
    return patch("h.services.auth_ticket.utcnow")
