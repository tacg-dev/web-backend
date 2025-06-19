s = "linkedin, linkedin.com\nlinkedin2, linkedni.com2"

def build_links(link_str: str):
    try:
        link_str = link_str.splitlines()
        links = [link.split(",") for link in link_str]
        d = {k.strip() : v.strip() for k,v in links}
        return d
    except Exception as e:
        return [""]


print(build_links(s))