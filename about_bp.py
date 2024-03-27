from flask import Blueprint, render_template

about_bp = Blueprint("about_bp", __name__)

users = [
    {
        "id": "1",
        "name": "Dhara",
        "pic": "https://i.pinimg.com/236x/db/b9/cb/dbb9cbe3b84da22c294f57cc7847977e.jpg",
        "pro": True,
    },
    {
        "id": "2",
        "name": "Yolanda",
        "pic": "https://images.pexels.com/photos/3792581/pexels-photo-3792581.jpeg?cs=srgb&dl=pexels-matheus-bertelli-3792581.jpg&fm=jpg",
        "pro": False,
    },
    {
        "id": "3",
        "name": "Nick",
        "pic": "https://assets.fxnetworks.com/cms-next/production/950c40a9-c758-426a-a2f9-be192d3fc395.jpg",
        "pro": True,
    },
]


# About page
@about_bp.route("/")
def about():
    return render_template("about.html", users=users)


# ----------------------------------------------------------------------------
@about_bp.route("/<id>")
def about_page_by_id(id):
    user = [user for user in users if user["id"] == id]
    return render_template("about.html", users=user)
