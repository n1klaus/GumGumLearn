import Tab from "react-bootstrap/Tab";
import Tabs from "react-bootstrap/Tabs";
import Accordion from "react-bootstrap/Accordion";
import SuggestionsMenu from "./Components/SuggestionsMenu";
import FilterMenu from "./Components/FilterMenu";

const SearchResults = ({ ...props }) => {
  return (
    <>
      <FilterMenu />
      <div className="container col-lg-4 col-12 col-md-6 col-sm-6 mb-4">
        <div
          className="searchResults"
          data-search-id={props.search_id}
          data-vault-id={props.vault_id}
        >
          <div>
            {props.word}
            {/* {props.pronunciations.audioFile} */}
            {/* {props.pronunciations.dialects} */}
            {/* {props.inflections} */}
          </div>
          <div className="lexicalCategory">
            <Tabs
              defaultActiveKey="0"
              id="lexical-categories-tab"
              className="mb-3"
              fill
              justify
            >
              {props.lexicalCategories.map((category, pos) =>
                // console.log(Object.keys(props))
                Object.keys(props).map((attr, loc) =>
                  // console.log(props[attr])
                  props[attr] !== undefined &&
                  props[attr].constructor === Object &&
                  category in props[attr] &&
                  props[attr][category].length > 0 ? (
                    <Tab eventKey={pos} title={category}>
                      <Accordion defaultActiveKey="0">
                        <Accordion.Item eventKey={loc}>
                          <Accordion.Header>{attr}</Accordion.Header>
                          <Accordion.Body>
                            <ol className="container">
                              {props[attr][category].map((item, index) =>
                                item !== undefined &&
                                (item.constructor !== Object ||
                                  item.constructor !== String) ? (
                                  <li key={index}>{item}</li>
                                ) : null
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
      <SuggestionsMenu />
    </>
  );
};
export default SearchResults;
