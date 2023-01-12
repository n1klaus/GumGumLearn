import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";

const Contact = () => {
  const submitForm = () => {};
  return (
    <>
      <div className="form-margin">
        <Form onSubmit={submitForm}>
          <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
            <Form.Label column sm="2">
              Username
            </Form.Label>
            <Col sm="3">
              <Form.Control
                id="username-box"
                type="text"
                placeholder="Enter username"
                required
              />
            </Col>
          </Form.Group>
          <Form.Group className="mb-3" controlId="exampleForm.ControlTextarea1">
            <Form.Label column sm="2">
              Enter text
            </Form.Label>
            <Col sm="3">
              <Form.Control id="comment-box" as="textarea" rows={3} required />
            </Col>
          </Form.Group>
        </Form>
        <Button variant="primary" type="submit">
          Submit
        </Button>
      </div>
    </>
  );
};

export default Contact;
