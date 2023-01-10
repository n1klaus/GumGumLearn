import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Offcanvas from 'react-bootstrap/Offcanvas';
import Languages from './Languages';
import Button from 'react-bootstrap/Button';

const Header = () => {
  return (
    <>
        <Navbar bg="light" expand="md" className="mb-3">
          <Container fluid>
            <Navbar.Brand href="/">GumGumLearn</Navbar.Brand>
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
                  <Nav.Link href="/about">About</Nav.Link>
                  <Nav.Link href="/contact">Contact</Nav.Link>
                  <NavDropdown
                    title="Language"
                    id={`offcanvasNavbarDropdown-expand-$sm`}
                  >
                    <Languages />
                  </NavDropdown>
                  <Nav.Link href="/login">
                    <Button>Login</Button>
                  </Nav.Link>
                </Nav>
              </Offcanvas.Body>
            </Navbar.Offcanvas>
          </Container>
        </Navbar>
    </>
  );
}
export default Header;
