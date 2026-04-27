"""
Onboarding()
FAQs()
Notifications()
News()
Events()
ServiceTypes(name, score:json)
Services(service_type, name, data:json, status, score, user)
Steps(user, created_at, updated_at, count)


Tasks:

1. Service types uchun model viewset
    (Get isauthenticated uchun qolgani admin uchun)

2. User service
    POST-ordinary user
    PUT-ordinary user if status is in_progress (own) | admin always change
    PATCH-ordinary user if status is in_progress (own) | admin always change
    DELETE | ordinary user if status is in_progress (own) | admin can do anything
    GET | ordinary user | can get all own | admin can get all of any services


django-filters

api/v1/services/?status=accepted&order_by=-date&q=asas, ordinary users-> hamma o'zini servicelarini beradi


"""
