import { useQuery } from "react-query";
import { useState } from "react";
import SearchResults from "../SearchResults";

const SearchHelper = ({ word }) => {
  const [search_data, setSearchData] = useState([]);
  const { isLoading, error } = useQuery("search_word", () =>
    fetch(`http://localhost:8000/search?text=${word}`)
      .then((res) => res.json())
      .then((res) => {
        setSearchData(res.data);
      })
  );
  if (isLoading) return "Loading...";
  if (error) return "An error occured: " + error.message;

  return (
    <div className="container">
      <section className="section">
        <div className="container">
          <div className="row">
            <div className="col-md-9">
              <div className="row">
                <>
                  {search_data
                    ? search_data.map((search_item, index) => (
                        <SearchResults
                          key={index}
                          word={search_item.word}
                          lexicalCategory={search_item.lexicalCategory}
                          translated_word={search_item.translated_word}
                          definitions={search_item.definitions}
                          pronunciations={search_item.pronunciations}
                          synonyms={search_item.synonyms}
                          antonyms={search_item.antonyms}
                          homophones={search_item.homophones}
                          examples={search_item.examples}
                          online_examples={search_item.online_examples}
                          search_id={search_item.search_id}
                          vault_id={search_item.vault_id}
                        />
                      ))
                    : console.error("Error mapping: " + typeof search_data)}
                </>
              </div>
            </div>
            <div className="col-md-3"></div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default SearchHelper;
