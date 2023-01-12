import { useNavigate } from "react-router";
import { fetchToken, setToken } from "./Components/Auth";
import React, { useState } from "react";
import axios from "axios";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Alert from "react-bootstrap/Alert";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

export default function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  //check to see if the fields are not empty
  const login = () => {
    if ((username === "") & (password === "")) {
      return;
    } else {
      axios
        .post("http://localhost:8000/login", {
          username: username,
          password: password,
        })
        .then(function (response) {
          console.log(response.data.token, "response.data.token");
          if (response.data.token) {
            setToken(response.data.token);
            navigate("/profile");
          }
        })
        .catch(function (error) {
          Alert("Login failed");
          console.error(error, "error");
        });
    }
  };
  return (
    <>
      <div className="d-block m-4">
        <div style={{ display: "flex", justifyContent: "center" }}>
          <h1>Login page</h1>
        </div>
        <div>
          {fetchToken() ? (
            <p>You are logged in</p>
          ) : (
            <div className="form-margin">
              <Form>
                <Form.Group
                  as={Row}
                  className="mb-3"
                  controlId="formBasicUsername"
                >
                  <Form.Label column sm="2">
                    Username
                  </Form.Label>
                  <Col sm="3">
                    <Form.Control
                      type="text"
                      placeholder="Enter username"
                      onChange={(e) => setUsername(e.target.value)}
                      required
                    />
                  </Col>
                </Form.Group>

                <Form.Group
                  as={Row}
                  className="mb-3 align-content-sm-center"
                  controlId="formBasicPassword"
                >
                  <Form.Label column sm="2">
                    Password
                  </Form.Label>
                  <Col sm="3">
                    <Form.Control
                      className="input-control"
                      type="password"
                      placeholder="Password"
                      onChange={(e) => setPassword(e.target.value)}
                      required
                    />
                  </Col>
                </Form.Group>
                <Col sm="6">
                  <Button variant="primary" type="submit" onClick={login}>
                    Log in
                  </Button>
                  <br></br>
                  <a href="/forgot_password">Forgot password?</a>
                  <br></br>
                  <a href="/signup">Signup</a>
                </Col>
              </Form>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
