import { ReactSearchAutocomplete } from "react-search-autocomplete";
import { useState } from "react";
import SearchHelper from "./Components/SearchHelper";

export default function Home() {
  const [search_text, setText] = useState();
  const items = [];

  const handleOnSearch = (string, results) => {
    // onSearch will have as the first callback parameter
    // the string searched and for the second the results.
    // const text_string = toString(string);
    console.log(`Search text: ${string}`);
    // results = "search_text"
    // console.log(`Results: ${results}`);
    setText(string);
  };

  const handleOnHover = (result) => {
    // the item hovered
    console.log(result);
  };

  const handleOnSelect = (item) => {
    // the item selected
    console.log(`Selected text: ${item}`);
  };

  const handleOnFocus = () => {
    const elem1 = document.querySelector(".search-bar");
    elem1.classList.remove("search-center");
    elem1.classList.add("search-top");
    const elem2 = document.querySelector(".footer-container");
    elem2.style = "visibility: hidden";
    console.log("Focused");
  };

  const formatResult = (item) => {
    return (
      <>
        <span style={{ display: "block", textAlign: "left" }}>
          match: {item.name}
        </span>
      </>
    );
  };
  return (
    <>
      <section className="search-bar search-center">
        <div>
          <ReactSearchAutocomplete
            items={items}
            inputDebounce={750}
            showNoResults={false}
            onSearch={handleOnSearch}
            onHover={handleOnHover}
            onSelect={handleOnSelect}
            onFocus={handleOnFocus}
            // autoFocus
            formatResult={formatResult}
          />
        </div>
      </section>
      <section className="search-results">
        {search_text ? <SearchHelper word={search_text} /> : null}
      </section>
    </>
  );
}
