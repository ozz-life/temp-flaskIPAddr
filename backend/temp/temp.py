#!/usr/bin/env python3

from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, IPAddress
from subprocess import check_output

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class InterfaceForm(FlaskForm):
    action = StringField("Action")
    ipaddress = StringField("IP Address", validators=[IPAddress()])
    netmask = StringField("Netmask", validators=[DataRequired()])
    submit = SubmitField("Save")


def get_credentials():
    credentials = {}
    with open("credentials.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split("=")
            if len(parts) == 2:
                credentials[parts[0]] = parts[1]
    return credentials


def check_credentials(username, password):
    credentials = get_credentials()
    return username == credentials.get("username") and password == credentials.get(
        "password"
    )


def login_required(func):
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


@app.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        if check_credentials(form.username.data, form.password.data):
            session["logged_in"] = True
            session["username"] = form.username.data
            return redirect("/home")
        else:
            error = "Invalid username or password."
    return render_template("login.html", form=form, error=error)


@app.route("/home")
@login_required
def home():
    return render_template("home.html", username=session["username"])


def run_command(command):
    output = check_output(command, shell=True)
    return output.decode()


def get_interface_state(interface_name):
    output = run_command(f"ip link show {interface_name}")
    parts = output.strip().split(" ")
    if "state" in parts:
        index = parts.index("state")
        if len(parts) > index + 1:
            return parts[index + 1]
    return None


def get_interface_address(interface_name):
    output = run_command(f"ip addr show {interface_name}")
    lines = output.strip().split("\n")
    for line in lines:
        parts = line.strip().split(" ")
        if parts[0] == "inet":
            return parts[1]
    return None


def get_interface_netmask(interface_name):
    output = run_command(f"ip addr show {interface_name}")
    lines = output.strip().split("\n")
    for line in lines:
        parts = line.strip().split(" ")
        if parts[0] == "inet":
            return parts[2]
    return None


@app.route("/interface/n", methods=["GET", "POST"])
# @app.route('/interface/<name>', methods=['GET', 'POST'])
@login_required
def interface(name):
    can_modify = session.get("can_modify")
    form = InterfaceForm()
    state = get_interface_state(name)
    ipaddress = get_interface_address(name)
    netmask = get_interface_netmask(name)

    if form.validate_on_submit():
        action = form.action.data
        if can_modify:
            if action == "up":
                run_command(f"sudo ip link set {name} up")
                flash(f"Started {name}.", "success")
            elif action == "down":
                run_command(f"sudo ip link set {name} down")
                flash(f"Stopped {name}.", "success")
            elif action == "save":
                ip = form.ipaddress.data
                netmask = form.netmask.data
                run_command(f"sudo ip addr add {ip}/{netmask} dev {name}")
                flash(f"Updated {name}.", "success")
            return redirect(url_for("interface", name=name))
        else:
            flash(f"You are not authorized to modify interfaces.", "warning")
            return redirect(url_for("interface", name=name))

    interface = {
        "name": name,
        "state": state,
        "ipaddress": ipaddress,
        "netmask": netmask,
    }
    return render_template(
        "interface.html", interface=interface, form=form, can_modify=can_modify
    )


if __name__ == "__main__":
    app.run()
