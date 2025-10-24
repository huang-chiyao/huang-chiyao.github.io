from pybtex.database.input import bibtex
from urllib.parse import urlparse, parse_qs

MEDIA_HEIGHT = 180  # put this near the top of your file (once)

def render_video(url: str) -> str:
    url_lower = url.lower()
    # YouTube
    if "youtube.com" in url_lower or "youtu.be" in url_lower:
        parsed = urlparse(url)
        video_id = None
        if "youtu.be" in parsed.netloc:
            video_id = parsed.path.lstrip("/")
        else:
            if parsed.path.startswith("/embed/"):
                video_id = parsed.path.split("/embed/")[1].split("/")[0]
            if not video_id:
                qs = parse_qs(parsed.query)
                video_id = (qs.get("v") or [None])[0]
        if not video_id:
            return f'<a href="{url}" target="_blank">Video</a>'
        return f'''
<div class="embed-responsive embed-responsive-16by9 my-2">
  <iframe class="embed-responsive-item"
          src="https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1&autoplay=1&mute=1&playsinline=1&loop=1"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen loading="lazy"></iframe>
</div>'''

    # Vimeo
    if "vimeo.com" in url_lower:
        video_id = url.rstrip("/").split("/")[-1].split("?")[0]
        return f'''
<div class="embed-responsive embed-responsive-16by9 my-2">
  <iframe class="embed-responsive-item"
          src="https://player.vimeo.com/video/{video_id}"
          allow="autoplay; fullscreen; picture-in-picture"
          allowfullscreen loading="lazy"></iframe>
</div>'''

    # Direct video files
    if url_lower.endswith((".mp4", ".webm", ".ogg")):
        return f'''
<video class="img-fluid my-2" controls preload="metadata">
  <source src="{url}">
  Your browser does not support the video tag.
</video>'''

    # Fallback: just a link
    return f'<a href="{url}" target="_blank">Video</a>'

def get_personal_data():
    name = ["Chi-Yao", "Huang"]
    email = "cy.huang@asu.edu"
    twitter = ""
    github = "huang-chiyao"
    linkedin = "chi-yao-huang"
    bio_text = f"""
        <p>Hello and welcome to my place. I'm Chi-Yao Huang.</p>

        <p>
            I am currently pursuing my Ph.D. under the guidance of Professor
            <a href="https://yezhouyang.engineering.asu.edu/" target="_blank"> Yezhou Yang</a> 
            at the School of Computing and Augmented Intelligence (SCAI), Arizona State University.
            Prior to joining ASU, I served as a pioneering VR/AR engineer at 
            <a href="https://www.vive.com/us/" target="_blank">VIVE</a> (now part of Google), where I developed innovative tracking technologies that power nearly all VIVE products.
            I also hold a master's degree in Mechanical Engineering from National Taiwan University.
        </p>

        <p>
            My research aims to develop a foundation model for spatial intelligence. I am focused on creating a <b>latent-centric</b> framework that unifies 3D geometry, semantics, and temporal dynamics, bridging the gap between classical VO/SLAM and the generative, queryable capabilities of modern large-scale models.
        </p>

        <p>
            <a href="https://huang-chiyao.github.io/assets/pdf/CV.pdf" target="_blank" style="margin-right: 15px">
                <i class="fa fa-address-card fa-lg"></i> CV
            </a>
            <a href="mailto:cy.huang@asu.edu" style="margin-right: 15px">
                <i class="far fa-envelope-open fa-lg"></i> Mail
            </a>
            <a href="https://twitter.com/chiyao_huang" target="_blank" style="margin-right: 15px">
                <i class="fab fa-twitter fa-lg"></i> Twitter
            </a>
            <a href="https://scholar.google.com/citations?user=YOUR_GOOGLE_SCHOLAR_ID" target="_blank" style="margin-right: 15px">
                <i class="fa-solid fa-book"></i> Scholar
            </a>
            <a href="https://github.com/huang-chiyao" target="_blank" style="margin-right: 15px">
                <i class="fab fa-github fa-lg"></i> Github
            </a>
            <a href="https://www.linkedin.com/in/chi-yao-huang" target="_blank" style="margin-right: 15px">
                <i class="fab fa-linkedin fa-lg"></i> LinkedIn
            </a>
        </p>
        """

    footer = """
            <div class="col-sm-12" style="">

            </div>
    """
    return name, bio_text, footer

def get_author_dict():
    return {
        'Yezhou Yang': 'https://yezhouyang.engineering.asu.edu/',
        'Zeel Bhatt': 'https://zeelbhatt.github.io/',
        }

def generate_person_html(persons, connection=", ", make_bold=True, make_bold_name='Chi-Yao Huang', add_links=True):
    links = get_author_dict() if add_links else {}
    s = ""
    for p in persons:
        string_part_i = ""
        for name_part_i in p.get_part('first') + p.get_part('last'): 
            if string_part_i != "":
                string_part_i += " "
            string_part_i += name_part_i
        if string_part_i in links.keys():
            string_part_i = f'<a href="{links[string_part_i]}" target="_blank">{string_part_i}</a>'
        if make_bold and string_part_i == make_bold_name:
            string_part_i = f'<span style="font-weight: bold";>{make_bold_name}</span>'
        if p != persons[-1]:
            string_part_i += connection
        s += string_part_i
    return s

def get_paper_entry(entry_key, entry):
    # safe fallbacks
    img_src = entry.fields.get('img', 'assets/img/default_project.jpg')
    video_url = entry.fields.get('video', '').strip()

    # Begin entry block
    s = """<div style="margin-bottom: 3em;">
    <div class="row">

    <!-- Left side: image + video side-by-side (wider column) -->
    <div class="col-sm-6">   <!-- increased from col-sm-4 -->
        <div class="row no-gutters align-items-center">
        <div class="col-5 pr-1">   <!-- image smaller -->
            <img src="{img_src}" class="img-fluid img-thumbnail" alt="Project image" style="max-width:100%;">
        </div>
    """.replace("{img_src}", img_src)

    # video part (same as before)
    if video_url:
        s += f"""
        <div class="col-7 pl-1 d-flex justify-content-center align-items-center">
            {render_video(video_url).replace('embed-responsive-16by9', 'embed-responsive-4by3').replace('my-2', 'my-0')}
        </div>
        """
    else:
        s += """<div class="col-7"></div>"""

    s += """
        </div>
    </div>

    <!-- Right side: text -->
    <div class="col-sm-6">   <!-- decreased from col-sm-8 -->
    """

    if 'award' in entry.fields.keys():
        s += f"""<a href="{entry.fields['html']}" target="_blank">{entry.fields['title']}</a> <span style="color: red;">({entry.fields['award']})</span><br>"""
    else:
        s += f"""<a href="{entry.fields['html']}" target="_blank">{entry.fields['title']}</a> <br>"""

    s += f"""{generate_person_html(entry.persons['author'])} <br>"""
    s += f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

    artefacts = {'html': 'Project Page', 'pdf': 'Paper', 'supp': 'Supplemental', 'video': 'Video', 'poster': 'Poster', 'code': 'Code'}

    i = 0
    for (k, v) in artefacts.items():
        if k in entry.fields.keys():
            if i > 0:
                s += ' / '
            s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1
        else:
            print(f'[{entry_key}] Warning: Field {k} missing!')

    cite = "<pre><code>@InProceedings{" + f"{entry_key}, \n"
    cite += "\tauthor = {" + f"{generate_person_html(entry.persons['author'], make_bold=False, add_links=False, connection=' and ')}" + "}, \n"
    for entr in ['title', 'booktitle', 'year']:
        cite += f"\t{entr} = " + "{" + f"{entry.fields[entr]}" + "}, \n"
    cite += """}</pre></code>"""
    s += " /" + f"""<button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse{entry_key}" aria-expanded="false" aria-controls="collapseExample" style="margin-left: -6px; margin-top: -2px;">Expand bibtex</button><div class="collapse" id="collapse{entry_key}"><div class="card card-body">{cite}</div></div>"""
    s += """ </div> </div> </div>"""
    return s

def get_talk_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""
    s += f"""{entry.fields['title']}<br>"""
    s += f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

    artefacts = {'slides': 'Slides', 'video': 'Recording'}
    i = 0
    for (k, v) in artefacts.items():
        if k in entry.fields.keys():
            if i > 0:
                s += ' / '
            s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1
        else:
            print(f'[{entry_key}] Warning: Field {k} missing!')
    s += """ </div> </div> </div>"""
    return s

def get_publications_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('publication_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s+= get_paper_entry(k, bib_data.entries[k])
    return s

def get_products_html():
    products = [
        {
            "name": "VIVE Focus 3",
            "img": "assets/img/vive_focus3.jpg",
            "video": "https://www.youtube.com/watch?v=xYEVcptQ33E",
            "desc": "Enterprise-grade mixed reality headset with high-resolution displays and ergonomic comfort.",
            "contrib": [
                "Developed the visual–inertial SLAM system for inside-out tracking.",
                "Designed multiple-camera motion estimation and sensor fusion algorithms.",
                "Collaborated with UX teams to optimize tracking for dynamic environments."
            ],
            "link": "https://www.vive.com/us/product/vive-focus3/overview/",
        },
        {
            "name": "VIVE XR Elite",
            "img": "assets/img/vive_xr_elite.jpg",
            "video": "https://www.youtube.com/watch?v=DKs5ncz4JlE",
            "desc": "Lightweight, modular XR headset built for immersive mixed reality experiences.",
            "contrib": [
                "Implemented visual–inertial odometry algorithms optimized for low-latency XR.",
                "Designed and prototyped the core data structures and processing pipeline for a mixed-reality system.",
                "Engineered an obstacle avoidance system to enhance user safety in mixed-reality environments."
            ],
            "link": "https://www.vive.com/us/product/vive-xr-elite/overview/",
        },
        {
            "name": "VIVE Flow",
            "img": "assets/img/vive_flow.jpg",
            "video": "https://www.youtube.com/watch?v=xzbRqENGjS0",
            "desc": "Compact, glasses-style VR headset designed for wellness, streaming, and portability.",
            "contrib": [
                "Designed the inside-out tracking algorithm for limited-FoV sensors.",
                "Developed a prototype motion tracking pipeline integrating a real-time hand-tracking system.",
                "Collaborated with optics and gaming teams to tune and optimize on-device performance."
            ],
            "link": "https://www.vive.com/us/product/vive-flow/overview/",
        },
    ]

    s = ""
    for product in products:
        img_src = product.get("img", "assets/img/default_project.jpg")
        video_url = product.get("video", "").strip()

        # Same layout as publications
        s += f"""<div style="margin-bottom: 3em;">
<div class="row">

  <!-- Left side: image + video -->
  <div class="col-sm-6">
    <div class="row no-gutters align-items-center">
      <div class="col-5 pr-1">
        <img src="{img_src}" class="img-fluid img-thumbnail" alt="{product['name']} image" style="max-width:100%;">
      </div>
"""
        # Video
        if video_url:
            s += f"""
      <div class="col-7 pl-1 d-flex justify-content-center align-items-center">
        {render_video(video_url).replace('embed-responsive-16by9', 'embed-responsive-4by3').replace('my-2', 'my-0')}
      </div>
"""
        else:
            s += """<div class="col-7"></div>"""

        # Right side: text + contributions
        s += f"""
    </div>
  </div>

  <!-- Right side: text -->
  <div class="col-sm-6">
    <a href="{product['link']}" target="_blank">{product['name']}</a> <br>
    <p>{product['desc']}</p>
"""
        # Contributions list
        if "contrib" in product and product["contrib"]:
            s += "<ul style='margin-top:-0.5em; margin-bottom:0.5em;'>"
            for item in product["contrib"]:
                s += f"<li>{item}</li>"
            s += "</ul>"

        s += """
  </div>
</div>
</div>
"""

    return s


def get_sponsors_html():
    sponsors = [
        {
            "name": "ASU Ira A. Fulton Schools of Engineering Fellowship",
            "short": "ASU Fulton Fellowship",
            "logo": "assets/img/sponsors/asu_fulton.png",
            "link": "https://engineering.asu.edu/",
        },
        {
            "name": "Toyota Research Institute of North America (TRINA)",
            "short": "TRINA",
            "logo": "assets/img/sponsors/toyota_trina.png",
            "link": "https://www.tri.global/",
        },
    ]

    s = """
<div style="margin-bottom: 1.5em;">
  <p class="mb-3">
    Chi-Yao is supported by the <strong>ASU Ira A. Fulton Schools of Engineering Fellowship</strong>
    and <strong>Toyota Research Institute of North America (TRINA)</strong>.
  </p>
  <div class="row text-center align-items-center justify-content-center">
"""

    # Consistent logo box
    for sp in sponsors:
        logo = sp["logo"]
        name = sp["name"]
        link = sp.get("link", "")
        s += f'''
    <div class="col-6 col-md-4 col-lg-3 mb-4 d-flex flex-column align-items-center">
      <div style="width:240px; height:150px; display:flex; justify-content:center; align-items:center; background:transparent;">
        <a href="{link}" target="_blank" rel="noopener" aria-label="{name}">
          <img src="{logo}" alt="{name} logo"
               style="max-width:240px; max-height:150px; object-fit:contain;">
        </a>
      </div>
      <div class="mt-2" style="font-size:0.95rem;">{sp["short"]}</div>
    </div>
'''

    s += """
  </div>
</div>
"""
    return s


def get_talks_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file('talk_list.bib')
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s+= get_talk_entry(k, bib_data.entries[k])
    return s


def get_index_html():
    pub = get_publications_html()
    # talks = get_talks_html()
    products = get_products_html()
    sponsors = get_sponsors_html()
    name, bio_text, footer = get_personal_data()
    
    s = f"""
    <!doctype html>
<html lang="en">

<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.0/css/all.min.css" integrity="sha512-xh6O/CkQoPOWDdYTDqeRdPCVd1SpvCA9XXcUnZS2FmJNp1coAFzvtCN9BmamE+4aHK8yyUHUSCcJHgXloTyT2A==" crossorigin="anonymous" referrerpolicy="no-referrer" />

  <title>{name[0] + ' ' + name[1]}</title>
  <link rel="icon" type="image/x-icon" href="assets/favicon.ico">
</head>

<body>
    <div class="container">
        <div class="row" style="margin-top: 3em;">
            <div class="col-sm-12" style="margin-bottom: 1em;">
            <h3 class="display-4" style="text-align: center;"><span">{name[0]}</span> {name[1]}</h3>
            </div>
            <br>
            <div class="col-md-8" style="">
                {bio_text}
            </div>
            <div class="col-md-4" style="">
                <img src="assets/img/profile.jpg" class="img-thumbnail" width="280px" alt="Profile picture">
            </div>
        </div>

        <div class="row" style="margin-top: 1em;">
            <div class="col-sm-12" style="">
                <h4>Publications</h4>
                {pub}
            </div>
        </div>

        <div class="row" style="margin-top: 3em;">
            <div class="col-sm-12" style="">
                <h4>Products</h4>
                {products}
            </div>
        </div>

        <div class="row" style="margin-top: 3em;">
            <div class="col-sm-12" style="">
                <h4>Sponsors &amp; Funding</h4>
                {sponsors}
            </div>
        </div>


        <div class="row" style="margin-top: 3em; margin-bottom: 1em;">
            {footer}
        </div>
    </div>

    <!-- Optional JavaScript -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
      integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
      crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
      integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7HUiibX39j7fakFPskvXusvfa0b4Q"
      crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
      integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
      crossorigin="anonymous"></script>
</body>

</html>
    """
    return s



def write_index_html(filename='index.html'):
    s = get_index_html()
    with open(filename, 'w') as f:
        f.write(s)
    print(f'Written index content to {filename}.')

if __name__ == '__main__':
    write_index_html('index.html')