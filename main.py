#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>Signup</h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

# test the vadility of username, password, and email
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)
PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)
def match_password(password, verify):
    return password == verify


class MainHandler(webapp2.RequestHandler):
    def get(self):
        form = """
        <form method="post">
            <table>
                <tr>
                    <td>
                        <label>Username</label>
                    </td>
                    <td>
                        <input type="text" name="username" value ="">
                    </td>
                </tr>

                <tr>
                    <td>
                        <label>Password</label>
                    </td>
                    <td>
                        <input type="password" name="password" value="">
                    </td>
                </tr>
                <tr>
                    <td>
                        <label>Verify Password</label>
                    </td>
                    <td>
                        <input type="password" name="verify" value="">
                    </td>
                </tr>
                <tr>
                    <td>
                        <label>Email (optional)</label>
                    </td>
                    <td>
                        <input type="email" name="email" value="">
                    </td>
                </tr>
            </table>
            <input type="submit" value="Submit">
        </form>
        """

        self.response.write(page_header + form + page_footer)

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        if valid_username(username) and valid_password(password) and match_password(password, verify) and valid_email(email):
            self.redirect("/welcome?username=" + username)

        if not valid_username(username):
            name_typed = ""
            name_error = "That's not a valid username."
        else:
            name_typed = username
            name_error = ""

        if not valid_password(password):
            password_error = "That's not a valid password."
        else:
            password_error =""

        if not match_password(password, verify):
            match_error = "Your passwords didn't match."
        else:
            match_error = ""

        if not valid_email(email):
            email_typed = ""
            email_error = "That's not a valid email."
        else:
            email_typed = email
            email_error = ""

        form = """
        <form method="post">
            <table>
                <tr>
                    <td>
                        <label>Username</label>
                    </td>
                    <td>
                        <input type="text" name="username" value="{n}">
                        <span class='error'>{n_error}</span>
                    </td>
                </tr>

                <tr>
                    <td>
                        <label>Password</label>
                    </td>
                    <td>
                        <input type="password" name="password" value="">
                        <span class='error'>{p_error}</span>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label>Verify Password</label>
                    </td>
                    <td>
                        <input type="password" name="verify" value="">
                        <span class='error'>{m_error}</span>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label>Email (optional)</label>
                    </td>
                    <td>
                        <input type="email" name="email" value="{e}">
                        <span class='error'>{e_error}</span>
                    </td>
                </tr>
            </table>
            <input type="submit" value="Submit">
        </form>
        """.format(n_error = name_error, n = name_typed, p_error = password_error, m_error = match_error, e = email_typed, e_error = email_error)

        self.response.write(page_header + form + page_footer)


class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        welcome_message = "<h3>" + "Welcome, " + username + "!" + "</h3>"
        self.response.write(welcome_message)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ("/welcome", Welcome)
], debug=True)
