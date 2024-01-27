from decimal import Decimal


def test_app_is_created(app):
    assert app.name == 'healthcare_bluestorm_system.app'
