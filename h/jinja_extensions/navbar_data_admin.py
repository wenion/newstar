from copy import deepcopy

from h.security import Permission


def navbar_data_admin(request):
    """
    Get the navigation bar displayed at the top of the admin page.

    This is used in `templates/layouts/admin.html.jinja2`
    """

    for tab in deepcopy(_ADMIN_MENU):
        if not request.has_permission(tab.pop("permission")):
            continue

        if route := tab.get("route"):
            tab["url"] = request.route_url(route)

        if children := tab.get("children"):
            for child in children:
                child["url"] = request.route_url(child["route"])

        yield tab


_ADMIN_MENU = [
    {
        "id": "index",
        "permission": Permission.AdminPage.LOW_RISK,
        "title": "Home",
        "route": "admin.index",
    },
    {
        "id": "admins",
        "permission": Permission.AdminPage.HIGH_RISK,
        "title": "Administrators",
        "route": "admin.admins",
    },
    {
        "id": "badge",
        "permission": Permission.AdminPage.HIGH_RISK,
        "title": "Badge",
        "route": "admin.badge",
    },
    {
        "id": "documents",
        "permission": Permission.AdminPage.HIGH_RISK,
        "title": "Documents",
        "route": "admin.documents",
    },
    {
        "id": "features",
        "permission": Permission.AdminPage.HIGH_RISK,
        "title": "Feature flags",
        "children": [
            {"route": "admin.features", "title": "Manage feature flags"},
            {"route": "admin.cohorts", "title": "Manage feature cohorts"},
        ],
    },
    {
        "id": "groups",
        "permission": Permission.AdminPage.LOW_RISK,
        "title": "Groups",
        "children": [
            {"route": "admin.groups", "title": "List Groups"},
            {"route": "admin.groups_create", "title": "Create a Group"},
        ],
    },
    {
        "id": "mailer",
        "permission": Permission.AdminPage.LOW_RISK,
        "title": "Mailer",
        "route": "admin.mailer",
    },
    {
        "id": "nipsa",
        "permission": Permission.AdminPage.HIGH_RISK,
        "title": "NIPSA",
        "route": "admin.nipsa",
    },
    {
        "id": "oauth",
        "permission": Permission.AdminPage.HIGH_RISK,
        "title": "OAuth clients",
        "route": "admin.oauthclients",
    },
    {
        "id": "organizations",
        "permission": Permission.AdminPage.LOW_RISK,
        "title": "Organizations",
        "children": [
            {"route": "admin.organizations", "title": "List organizations"},
            {"route": "admin.organizations_create", "title": "Create an organization"},
        ],
    },
    {
        "id": "staff",
        "permission": Permission.AdminPage.HIGH_RISK,
        "title": "Staff",
        "route": "admin.staff",
    },
    {
        "id": "users",
        "permission": Permission.AdminPage.LOW_RISK,
        "title": "Account",
        "children": [
            {"route": "admin.users", "title": "Find users"},
            {"route": "admin.batch_users", "title": "List users"},
            {"route": "admin.users_create", "title": "Create an account"},
        ],
    },
    {
        "id": "search",
        "permission": Permission.AdminPage.HIGH_RISK,
        "title": "Search",
        "route": "admin.search",
    },
    {
        "id": "locations",
        "permission": Permission.AdminPage.LOW_RISK,
        "title": "Locations",
        "children": [
            {"route": "admin.locations", "title": "List locations"},
            {"route": "admin.locations_create", "title": "Create a location"},
        ],
    },
    {
        "id": "levels",
        "permission": Permission.AdminPage.LOW_RISK,
        "title": "Levels",
        "children": [
            {"route": "admin.levels", "title": "List levels"},
            {"route": "admin.levels_create", "title": "Create a level"},
        ],
    },
    {
        "id": "terms",
        "permission": Permission.AdminPage.LOW_RISK,
        "title": "Terms",
        "children": [
            {"route": "admin.terms", "title": "List terms"},
            {"route": "admin.terms_create", "title": "Create a term"},
        ],
    },
    {
        "id": "courses",
        "permission": Permission.AdminPage.LOW_RISK,
        "title": "Courses",
        "children": [
            {"route": "admin.courses", "title": "List courses"},
            {"route": "admin.courses_create", "title": "Create a course"},
        ],
    },
    {
        "id": "plans",
        "permission": Permission.AdminPage.LOW_RISK,
        "title": "Plans",
        "children": [
            {"route": "admin.batch_plans", "title": "List batch plans"},
            {"route": "admin.plans", "title": "List plans"},
            {"route": "admin.plans_create", "title": "Create a plan"},
        ],
    },
    {
        "id": "registrations",
        "permission": Permission.AdminPage.LOW_RISK,
        "title": "Registrations",
        "children": [
            {"route": "admin.registration_term_options", "title": "List term options"},
            {"route": "admin.registration_term_options_create", "title": "Create a term option"},
            {"route": "admin.registration_source_options", "title": "List source options"},
            {"route": "admin.registration_source_options_create", "title": "Create a source"},
            {"route": "admin.registrations", "title": "List registrations"},
            {"route": "admin.registrations_create", "title": "Create a registration"},
        ],
    },
    {
        "id": "profiles",
        "permission": Permission.AdminPage.LOW_RISK,
        "title": "Profiles",
        "children": [
            {"route": "admin.profiles", "title": "List profiles"},
            {"route": "admin.profiles_create", "title": "Create a profile"},
        ],
    },
    {
        "id": "items",
        "permission": Permission.AdminPage.LOW_RISK,
        "title": "Items",
        "children": [
            {"route": "admin.cost_items", "title": "List items"},
            {"route": "admin.cost_items_create", "title": "Create an item"},
        ],
    },
]
