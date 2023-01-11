import Tab from "react-bootstrap/Tab";
import Tabs from "react-bootstrap/Tabs";
import Accordion from "react-bootstrap/Accordion";

const SearchResults = ({ ...props }) => {
  return (
    <div className="col-lg-4 col-12 col-md-6 col-sm-6 mb-5">
      <div
        className="searchResults"
        data-search-id={props.search_id}
        data-vault-id={props.vault_id}
      >
        <div className="nounCategory">
          <Tabs
            defaultActiveKey="0"
            id="uncontrolled-tab-example"
            className="mb-3"
            fill
            justify
          >
            {props.word}
            {props.lexicalCategory}
            {/* {props.pronunciations} */}
            {["Noun", "Verb", "Adjective", "Adverb"].map((category, pos) =>
              // console.log(Object.keys(props))
              Object.keys(props).map((obj, loc) =>
                // console.log(props[obj])
                props[obj] !== undefined &&
                props[obj].constructor === Object &&
                category in props[obj] &&
                props[obj][category].length > 0 ? (
                  <Tab eventKey={pos} title={category}>
                    <Accordion defaultActiveKey="0">
                      <Accordion.Item eventKey={loc}>
                        <Accordion.Header>{obj}</Accordion.Header>
                        <Accordion.Body>
                          <ol>
                            {props[obj][category].map((item, index) =>
                              item !== undefined &&
                              item.constructor === Object ? (
                                console.log(Object.values(item))
                              ) : (
                                <li key={index}>{item}</li>
                              )
                            )}
                          </ol>
                        </Accordion.Body>
                      </Accordion.Item>
                    </Accordion>
                  </Tab>
                ) : null
              )
            )}
          </Tabs>
        </div>
      </div>
    </div>
  );
};
export default SearchResults;
