import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Offcanvas from 'react-bootstrap/Offcanvas';

export default function Header() {
  return (
    <>
        <Navbar bg="light" expand="md" className="mb-3">
          <Container fluid>
            <Navbar.Brand href="#">GumGumLearn</Navbar.Brand>
            <Navbar.Toggle aria-controls={`offcanvasNavbar-expand-$sm`} />
            <Navbar.Offcanvas
              id={`offcanvasNavbar-expand-$sm`}
              aria-labelledby={`offcanvasNavbarLabel-expand-$sm`}
              placement="end"
            >
              <Offcanvas.Header closeButton>
                <Offcanvas.Title id={`offcanvasNavbarLabel-expand-$sm`}>
                  More
                </Offcanvas.Title>
              </Offcanvas.Header>
              <Offcanvas.Body>
                <Nav className="justify-content-end flex-grow-1 pe-3">
                  <Nav.Link href="#action1">About</Nav.Link>
                  <Nav.Link href="#action2">Contact</Nav.Link>
                  <NavDropdown
                    title="Language"
                    id={`offcanvasNavbarDropdown-expand-$sm`}
                  >
                    <NavDropdown.Item href="#action3">Action</NavDropdown.Item>
                    <NavDropdown.Item href="#action4">
                      Another action
                    </NavDropdown.Item>
                    <NavDropdown.Divider />
                    <NavDropdown.Item href="#action5">
                      Something else here
                    </NavDropdown.Item>
                  </NavDropdown>
                </Nav>
              </Offcanvas.Body>
            </Navbar.Offcanvas>
          </Container>
        </Navbar>
    </>
  );
}
