ROLE_GUEST = "guest"
ROLE_USER = "user"
ROLE_MANAGER = "manager"
ROLE_ADMIN = "admin"

PERMISSIONS = {
    ROLE_GUEST: {
        "view_products": True,
        "buy_products": False,
        "edit_products": False,
        "manage_users": False,
        "view_orders": False,
    },
    ROLE_USER: {
        "view_products": True,
        "buy_products": True,
        "edit_products": False,
        "manage_users": False,
        "view_orders": True,
    },
    ROLE_MANAGER: {
        "view_products": True,
        "buy_products": False,
        "edit_products": True,
        "manage_users": False,
        "view_orders": True,
    },
    ROLE_ADMIN: {
        "view_products": True,
        "buy_products": True,
        "edit_products": True,
        "manage_users": True,
        "view_orders": True,
    },
}
