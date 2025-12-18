# University Logo Setup Guide

## Quick Start

You need to add university logo images to display them on the country universities page.

## Step 1: Get University Logos

### Option A: Download from Official Sources
Visit each university's official website and download their logo from their press/media kit section:
- Harvard: https://www.harvard.edu/media-relations/guidelines-for-use-of-the-harvard-name-and-logo
- Stanford: https://identity.stanford.edu/
- MIT: https://communications.mit.edu/guidelines/logos-and-wordmarks
- Oxford: https://www.ox.ac.uk/public-affairs/brand-toolkit
- Cambridge: https://www.cam.ac.uk/brand-resources/about-the-logo

### Option B: Use Free Logo Resources
- Wikimedia Commons (public domain logos)
- Universities' official Wikipedia pages
- clearbit.com/logo (for some universities)

### Option C: Create Placeholder Icons
If you can't find logos, create simple placeholder images with:
- University initials (e.g., "H" for Harvard)
- Solid background color
- White text

## Step 2: Prepare Logo Images

### Requirements
- **Format:** PNG (transparent background preferred)
- **Size:** 200x200px minimum (400x400px recommended)
- **Quality:** High resolution
- **Background:** Transparent or white

### File Naming Convention
Use the university slug as the filename:

```
harvard.png          → Harvard University
stanford.png         → Stanford University
mit.png              → Massachusetts Institute of Technology
oxford.png           → Oxford University
cambridge.png        → Cambridge University
yale.png             → Yale University
princeton.png        → Princeton University
columbia.png         → Columbia University
upenn.png            → University of Pennsylvania
dartmouth.png        → Dartmouth College
brown.png            → Brown University
cornell.png          → Cornell University
caltech.png          → California Institute of Technology
uchicago.png         → University of Chicago
duke.png             → Duke University
northwestern.png     → Northwestern University
jhu.png              → Johns Hopkins University
vanderbilt.png       → Vanderbilt University
rice.png             → Rice University
notre-dame.png       → University of Notre Dame
ucberkeley.png       → UC Berkeley
ucla.png             → UCLA
usc.png              → USC
unc.png              → UNC Chapel Hill
umich.png            → University of Michigan
```

## Step 3: Upload Logos

### Method 1: Manual Upload (Simple)
1. Navigate to your project directory:
   ```bash
   cd /home/saidi/Projects/Global-agency/static/global_agency/img/university-logos/
   ```

2. Copy your PNG files to this directory

3. Verify files are named correctly (lowercase, hyphens for spaces)

### Method 2: Command Line (Advanced)
```bash
# From project root
cd /home/saidi/Projects/Global-agency

# Create symbolic links if logos are in another directory
ln -s /path/to/your/logos/*.png static/global_agency/img/university-logos/

# Or copy files
cp /path/to/your/logos/*.png static/global_agency/img/university-logos/
```

## Step 4: Collect Static Files

After adding logos, collect static files for Django:

```bash
cd /home/saidi/Projects/Global-agency
source env/Scripts/activate  # Windows
# OR
source env/bin/activate      # Linux/Mac

python manage.py collectstatic --noinput
```

## Step 5: Verify Display

1. Start your development server:
   ```bash
   python manage.py runserver
   ```

2. Navigate to: http://localhost:8000/universities/countries/

3. Check if logos appear on university cards

4. If a logo doesn't appear, verify:
   - File exists in the directory
   - Filename matches university slug exactly
   - File is a valid PNG image
   - Static files were collected

## Fallback Behavior

If a logo image is missing or fails to load:
- ✅ University icon (🏛️) will display instead
- ✅ University name shown below icon
- ✅ No broken image icons
- ✅ Page functions normally

## Troubleshooting

### Logo Not Displaying?

**Check 1: File Path**
```bash
ls -la static/global_agency/img/university-logos/
```
Should show your PNG files.

**Check 2: File Permissions**
```bash
chmod 644 static/global_agency/img/university-logos/*.png
```

**Check 3: Django Static Files**
```python
# In Django shell
python manage.py shell
>>> from django.conf import settings
>>> print(settings.STATIC_URL)
>>> print(settings.STATIC_ROOT)
```

**Check 4: Browser Console**
- Open browser DevTools (F12)
- Check Console for 404 errors
- Check Network tab for failed image requests

**Check 5: Hard Refresh**
- Clear browser cache
- Hard refresh (Ctrl + Shift + R or Cmd + Shift + R)

### Creating Placeholder Logos Quickly

If you need placeholder logos fast:

**Using ImageMagick (Command Line):**
```bash
# Install ImageMagick first
sudo apt-get install imagemagick  # Linux
# OR
brew install imagemagick          # Mac

# Create placeholder logos
convert -size 400x400 xc:blue -gravity center \
        -pointsize 100 -fill white -annotate +0+0 "H" \
        static/global_agency/img/university-logos/harvard.png

convert -size 400x400 xc:red -gravity center \
        -pointsize 100 -fill white -annotate +0+0 "S" \
        static/global_agency/img/university-logos/stanford.png
```

**Using Python (PIL/Pillow):**
```python
from PIL import Image, ImageDraw, ImageFont

def create_logo(letter, color, filename):
    img = Image.new('RGB', (400, 400), color=color)
    draw = ImageDraw.Draw(img)
    
    # Use default font or specify path to .ttf file
    try:
        font = ImageFont.truetype("arial.ttf", 200)
    except:
        font = ImageFont.load_default()
    
    # Center text
    bbox = draw.textbbox((0, 0), letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((400 - text_width) // 2, (400 - text_height) // 2)
    
    draw.text(position, letter, fill='white', font=font)
    img.save(f'static/global_agency/img/university-logos/{filename}')

# Create placeholders
create_logo('H', '#A51C30', 'harvard.png')  # Harvard crimson
create_logo('S', '#8C1515', 'stanford.png')  # Stanford red
create_logo('M', '#750014', 'mit.png')       # MIT red
```

**Using Online Tools:**
- Canva.com (free, easy)
- Figma.com (free, professional)
- photopea.com (free Photoshop alternative)

## Batch Logo Creation Script

Save this as `create_placeholder_logos.py`:

```python
from PIL import Image, ImageDraw, ImageFont
import os

LOGOS_DIR = 'static/global_agency/img/university-logos/'
os.makedirs(LOGOS_DIR, exist_ok=True)

UNIVERSITIES = {
    'harvard': ('H', '#A51C30'),
    'stanford': ('S', '#8C1515'),
    'mit': ('M', '#750014'),
    'oxford': ('O', '#002147'),
    'cambridge': ('C', '#A3C1AD'),
    'yale': ('Y', '#00356B'),
    'princeton': ('P', '#FF8F00'),
}

for slug, (letter, color) in UNIVERSITIES.items():
    img = Image.new('RGB', (400, 400), color=color)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 200)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((400 - text_width) // 2, (400 - text_height) // 2)
    
    draw.text(position, letter, fill='white', font=font)
    img.save(os.path.join(LOGOS_DIR, f'{slug}.png'))
    print(f'Created {slug}.png')

print('All placeholder logos created!')
```

Run with:
```bash
pip install pillow
python create_placeholder_logos.py
```

## Best Practices

1. **Always use official logos** when possible (respect copyright)
2. **Maintain aspect ratio** - don't stretch logos
3. **Use transparent backgrounds** - looks better on different backgrounds
4. **Optimize file size** - use tools like TinyPNG.com
5. **Test on mobile** - ensure logos are readable at small sizes
6. **Keep backups** - save original high-res versions

## License Considerations

⚠️ **Important:** University logos are typically trademarked. 

**Guidelines:**
- ✅ OK: Educational/informational use (like student portals)
- ✅ OK: Non-commercial use with proper attribution
- ❌ NOT OK: Commercial use without permission
- ❌ NOT OK: Modifying official logos
- ❌ NOT OK: Implying university endorsement

**Safe approach:**
1. Use official logos from university press kits
2. Follow their brand guidelines
3. Add disclaimer: "University logos are trademarks of their respective institutions"

---

**Need Help?**
- Check Django logs: `logs/django.log`
- Test in browser: http://localhost:8000/universities/countries/
- Verify file exists: `ls static/global_agency/img/university-logos/`
