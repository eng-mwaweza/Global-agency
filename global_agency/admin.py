from django.contrib import admin
from .models import ContactMessage, StudentApplication


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at', 'handled')
    list_filter = ('handled', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    ordering = ('-created_at',)


@admin.register(StudentApplication)
class StudentApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'email',
        'phone',
        'nationality',
        'created_at',
    )
    search_fields = (
        'full_name',
        'email',
        'phone',
        'father_name',
        'mother_name',
        'emergency_name',
    )
    list_filter = (
        'gender',
        'nationality',
        'emergency_gender',
        'created_at',
    )
    ordering = ('-created_at',)

    fieldsets = (
        ('Personal Information', {
            'fields': (
                'full_name', 'gender', 'nationality', 'email', 'phone', 'address'
            )
        }),
        ('Parents Details', {
            'fields': (
                'father_name', 'father_phone', 'father_email', 'father_occupation',
                'mother_name', 'mother_phone', 'mother_email', 'mother_occupation'
            ),
            'classes': ('collapse',)
        }),
        ('Education Background - O-Level', {
            'fields': (
                'olevel_school', 'olevel_country', 'olevel_address', 'olevel_region',
                'olevel_year', 'olevel_candidate_no', 'olevel_gpa'
            ),
            'classes': ('collapse',)
        }),
        ('Education Background - A-Level', {
            'fields': (
                'alevel_school', 'alevel_country', 'alevel_address', 'alevel_region',
                'alevel_year', 'alevel_candidate_no', 'alevel_gpa'
            ),
            'classes': ('collapse',)
        }),
        ('Study Preferences', {
            'fields': (
                'preferred_country_1', 'preferred_country_2', 'preferred_country_3', 'preferred_country_4',
                'preferred_program_1', 'preferred_program_2', 'preferred_program_3', 'preferred_program_4'
            ),
            'classes': ('collapse',)
        }),
        ('Emergency Contact', {
            'fields': (
                'emergency_name', 'emergency_address', 'emergency_occupation',
                'emergency_gender', 'emergency_relation', 'heard_about_us', 'heard_about_other'
            ),
            'classes': ('collapse',)
        }),
        ('System Info', {
            'fields': ('created_at',),
        }),
    )

    readonly_fields = ('created_at',)
