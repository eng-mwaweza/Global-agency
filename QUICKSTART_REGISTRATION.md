# Quick Start Guide - New Registration System

## For Users

### Creating a New Account

1. **Visit the homepage** at `http://your-domain.com/`

2. **Click "Create Account Now"** (yellow button at bottom-right) or "Create Account" in the navigation

3. **Fill the simple registration form:**
   - Full Name
   - Email Address
   - Password (min 8 characters)
   - Confirm Password

4. **Click "Create Account"** → You'll see: "Account created successfully! Please login with your email: [your-email]"

5. **Click "Login here"** or go to Student Portal

6. **Login** with:
   - Username: Your email address
   - Password: Your password

7. **Complete your profile** step-by-step:
   - **Personal Details** (required): Add your personal information
   - **Parents Details** (recommended): Add your parents' information
   - **Academic Qualifications** (required): O-Level and A-Level details
   - **Study Preferences** (required): Choose up to 4 study destinations
   - **Emergency Contact** (required): Provide emergency contact information

8. **Track your progress** - Watch the completion bar in the sidebar!

9. **Once complete** - You can start creating applications!

## For Administrators

### Testing the New System

1. **Start the development server:**
   ```bash
   cd /home/saidi/Projects/Global-agency
   source .venv/bin/activate  # or: .venv/bin/activate
   python manage.py runserver
   ```

2. **Access the application:**
   - Homepage: http://127.0.0.1:8000/
   - Registration: http://127.0.0.1:8000/register/
   - Student Login: http://127.0.0.1:8000/student/login/
   - Dashboard: http://127.0.0.1:8000/student/ (after login)

3. **Test the registration flow:**
   - Create a new account
   - Login with the new account
   - Complete each profile section
   - Verify data saves correctly
   - Check completion percentage updates

### Key URLs

| Page | URL | Description |
|------|-----|-------------|
| Homepage | `/` | Main landing page |
| Registration | `/register/` | New account creation |
| Student Login | `/student/login/` | Login page |
| Dashboard | `/student/` | Main dashboard (after login) |
| Personal Details | `/student/profile/personal-details/` | Personal info form |
| Parents Details | `/student/profile/parents-details/` | Parents info form |
| Academic Qualifications | `/student/profile/academic-qualifications/` | Education details |
| Study Preferences | `/student/profile/study-preferences/` | Study destination choices |
| Emergency Contact | `/student/profile/emergency-contact/` | Emergency contact info |

### Database

**Migration applied:**
```bash
python manage.py migrate student_portal
```

**Check migration status:**
```bash
python manage.py showmigrations student_portal
```

**Latest migration:**
- `0007_studentprofile_academic_qualifications_complete_and_more.py`
- Added 50+ fields to StudentProfile
- Added completion tracking fields

### Verification

**Run the test script:**
```bash
python test_registration_implementation.py
```

**Expected output:**
```
✅ ALL TESTS PASSED!

📋 Implementation Summary:
   • SimpleRegistrationForm: ✅
   • 5 Profile Section Forms: ✅
   • StudentProfile Model Extended: ✅
   • Completion Tracking: ✅

🚀 Ready for testing in browser!
```

**Django system check:**
```bash
python manage.py check
```

Should show: `System check identified no issues (0 silenced).`

### Troubleshooting

**Issue: "No module named 'student_portal'"**
- Solution: Ensure you're in the project directory and virtual environment is activated

**Issue: "TemplateDoesNotExist"**
- Solution: Check that all template files exist in `student_portal/templates/student_portal/`

**Issue: "relation does not exist"**
- Solution: Run migrations: `python manage.py migrate student_portal`

**Issue: Forms don't display correctly**
- Solution: Clear browser cache, check Tailwind CDN is loading

**Issue: Profile completion doesn't update**
- Solution: Check that all required fields are filled in each section

### Logs

Check logs for errors:
- Django: `logs/django.log`
- Errors: `logs/django_errors.log`
- Security: `logs/security.log`

### Rollback (If Needed)

If you need to rollback to the old system:

1. **Revert URL changes:**
   - Change `/register/` back to `/start-application/` in homepage
   - Update navigation links in base.html

2. **Keep using old route:**
   - Old route still works at `/start-application/`
   - Just update links to point there

3. **Database is safe:**
   - Old StudentApplication table unchanged
   - New StudentProfile fields are additive (won't break existing data)

## Features Overview

### ✅ Simple Registration
- Just 4 fields (name, email, password)
- Email validation (no duplicates)
- Password confirmation
- Instant account creation

### ✅ Progressive Profile Completion
- Split into 5 manageable sections
- Save and resume anytime
- Clear progress tracking
- Visual completion percentage

### ✅ Modern Dashboard
- Sidebar navigation
- Profile picture display
- Completion checkmarks
- Easy section access

### ✅ User-Friendly Forms
- Helpful placeholders
- Field-level validation
- Error messages
- Clear instructions

### ✅ Mobile Responsive
- Works on all screen sizes
- Touch-friendly interface
- Optimized layouts

## Support

**Documentation:**
- Full implementation details: `REGISTRATION_REDESIGN_SUMMARY.md`
- This quick start guide: `QUICKSTART_REGISTRATION.md`

**Questions or Issues?**
1. Check the logs in `logs/` directory
2. Run `python manage.py check` for system issues
3. Run `python test_registration_implementation.py` for verification
4. Review error messages in browser console

---

**Status: ✅ Production Ready**

Last Updated: December 17, 2025
Version: 1.0
