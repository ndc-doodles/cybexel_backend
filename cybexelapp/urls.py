from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('about', views.about, name='about'),  
    path('blog', views.blog, name='blog'),
    path('careers', views.careers, name='careers'),
    path('contact', views.contact, name='contact'),
    path('services', views.services, name='services'),
    path('cybexel_life', views.cybexel_life, name='cybexel_life'),
    path('life-event/<int:pk>/', views.detail, name='life_event_detail'),



    


    # path('admin_register/', views.admin_register, name='admin_register'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.admin_logout, name='logout'),
    # path('edit-client-logo/<int:id>/', views.edit_client_logo, name='edit_client_logo'),
    path('delete-client-logo/<int:id>/', views.delete_client_logo, name='delete_client_logo'),
    path('stat/update/', views.update_stat, name='update_stat'),
    path('stat/add/', views.add_stat, name='add_stat'),  # <-- Fix this line
    path('admin_contact/', views.admin_contact, name='admin_contact'),
    path('bulk_delete_contacts/', views.bulk_delete_contacts, name='bulk_delete_contacts'),
    path("admin_blog/", views.admin_blog, name="admin_blog"),
    path("delete-blog/<int:id>/", views.delete_blog, name="delete_blog"),
    path('get-blog/<int:blog_id>/', views.get_blog, name='get_blog'),
    path("update-blog/", views.update_blog, name="update_blog"),
    path('admin_careers', views.admin_careers, name='admin_careers'),
    path('submit_job_application/', views.submit_job_application, name='submit_application'),

    path("delete-department/<int:pk>/", views.delete_department, name="delete_department"),
    path("delete-experience/<int:pk>/", views.delete_experience, name="delete_experience"),
    path("delete-job/<int:pk>/", views.delete_job, name="delete_job"),

    path("edit-department/<int:pk>/", views.edit_department, name="edit_department"),
    path("edit-experience/<int:pk>/", views.edit_experience, name="edit_experience"),
    path("edit-job/<int:pk>/", views.edit_job, name="edit_job"),
    path('delete_job_application/<int:id>/', views.delete_job_application, name='delete_job_application'),
    path('admin_job_applications/', views.admin_job_applications, name='admin_job_applications'),
    path('bulk_delete_job_applications/', views.bulk_delete_job_applications, name='bulk_delete_job_applications'),
    path('admin_cybexelife/', views.admin_cybexelife, name='admin_cybexelife'),
    path('custom-admin/delete-event/<int:event_id>/', views.delete_event, name='delete_Event'),
    path('get-event-images/<int:event_id>/', views.get_event_images, name='get_event_images'),
    path('delete-event-image/<int:id>/', views.delete_event_image, name='delete_event_image'),
    
]
