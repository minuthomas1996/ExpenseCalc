from django.urls import path

import expense.views

urlpatterns = [
    path('',expense.views.index,name='index'),
    path('index',expense.views.index,name='index'),
    path('register',expense.views.register,name='register'),
    path('add_expense',expense.views.add_expense,name='add_expense'),
    path('view_expense',expense.views.view_expense,name='view_expense'),

    # path('user_home',expense.views.user_home,name='user_home'),

    path('filter_expense',expense.views.filter_expense,name='filter_expense'),
    path('edit_expense/<id>/',expense.views.edit_expense,name='edit_expense'),
    path('delete_expense\<id>',expense.views.delete_expense,name='delete_expense'),

    # path('admin_home',expense.views.admin_home,name='admin_home'),
    path('expense_list',expense.views.expense_list,name='expense_list'),
    path('admin_filter_expense',expense.views.admin_filter_expense,name='admin_filter_expense'),

    path('admin_edit_expense\<id>',expense.views.admin_edit_expense,name='admin_edit_expense'),
    path('admin_delete_expense\<id>',expense.views.admin_delete_expense,name='admin_delete_expense'),

    path('users_list',expense.views.users_list,name='users_list'),
    path('approve\<id>',expense.views.approve,name='approve'),

    path('logout',expense.views.logout,name='logout'),
    path('forgotpassword',expense.views.forgotpassword,name='forgotpassword'),
    # path('sendingmail',expense.views.sendingmail,name='sendingmail'),
    ]