import { useNavigate } from "react-router";
import { fetchToken, setToken } from "./Components/Auth";
import { useState } from "react";
import axios from "axios";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";

export default function ResetPassword() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");

  //check to see if the fields are not empty
  const resetPassword = () => {
    if (username === "") {
      return;
    } else {
      axios
        .post("http://localhost:8000/forgot_password", {
          username: username,
        })
        .then(function (response) {
          console.log(response.data.token, "response.data.token");
          if (response.data.token) {
            setToken(response.data.token);
            navigate("/");
          }
        })
        .catch(function (error) {
          console.log(error, "error");
        });
    }
  };
  return (
    <div style={{ minHeight: 800, marginTop: 30 }}>
      <h1>Reset password page</h1>
      <div style={{ marginTop: 30 }}>
        {fetchToken() ? (
          navigate("/")
        ) : (
          <div>
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

              <Col sm="6">
                <Button variant="primary" type="submit" onClick={resetPassword}>
                  Reset Password
                </Button>
                <br></br>
                <a href="/login">Log in</a>
              </Col>
            </Form>
          </div>
        )}
      </div>
    </div>
  );
}
