import Card from "react-bootstrap/Card";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";

const About = () => {
  return (
    <div className="container">
      <Card className="m-4">
        <Card.Img
          className="image-margin"
          variant="top"
          src="./assets/images/cover_image.jpg"
        />
        <Card.Body>
          <blockquote className="blockquote mb-0">
            <p>
              {" "}
              It is what we know already that often prevents us from learning.{" "}
            </p>
            <footer className="blockquote-footer">
              Claude Bernard{" "}
              <cite title="Source Title">
                {" "}
                <a href="https://www.brainyquote.com/quotes/claude_bernard_177950">
                  Brainy Quote
                </a>
              </cite>
            </footer>
          </blockquote>
        </Card.Body>
      </Card>
      <Row xs={1} md={2} className="g-3">
        <Col className="mt-2 mb-2">
          <Card>
            <Card.Body>
              <Card.Title>About</Card.Title>
              <Card.Text>
                Languages are immensely complicated structures. One soon
                realizes how complicated any language is when trying to learn it
                as a second language. If one tries to frame an exhaustive
                description of all the rules embodied in one’s language—the
                rules by means of which a native user is able to produce and
                understand an infinite number of correct well-formed
                sentences—one can easily appreciate the complexity of the
                knowledge that a child acquires while mastering a native
                vernacular. The descriptions of languages written so far are in
                most cases excellent as far as they go, but they still omit more
                than they contain of an explicit account of native users’
                competence in their language, whether that language is English,
                Swahili, or Japanese Sign Language
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
        <Col className="mt-2 mb-2">
          <Card>
            <Card.Body>
              <Card.Title>Inspiration</Card.Title>
              <Card.Text>
                This project was inspired by my need to track and learn new
                words i always encountered when reading books or in online
                publications. It was always easy to highlight on a hard cover
                but hard to recollect something that struck your mind at a
                particular time. After a shift to Pdfs and online books the
                hassle got easier but not completely eradicated. In the process
                of finishing up a book i always wanted to be able to apply some
                of the new words but i had no strategy for that. Hence later on
                i decided to create a key-value storage file to store words and
                their meanings and synonyms so that if i encountered for example
                two new similar words I would be able to make the connection.
                With time i added features like pronunciation and translation up
                to this point where i have aggregated all that trial and error
                into a web application on a broader scope to help learners or
                people facing the same challenges and also with extra features.
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default About;
