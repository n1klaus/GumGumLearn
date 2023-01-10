/* eslint-disable jsx-a11y/anchor-is-valid */
import React, { useEffect, useState } from "react";
import {useQuery} from 'react-query'
import SearchResults from "./SearchResults";

// const SearchContext = React.createContext({
// 	search_items: [],
// 	fetchItems: () => {}
// })

const SearchHelper = ({word}) => {
	// const [search_items, setItems] = useState([])
	// const {search_items, fetchItems} = React.useContext(ProductsContext)

	const {isLoading, error, search_items } = useQuery("search_word", () =>
		// console.log(`word to search: ${word}`);
		// if (word !== undefined || word !== '') {
			fetch(`http://localhost:8000/search?text=${word}`)
			.then(res => res.json())
			.then(res => {return Array(res.data)})
			// console.log(search_items.data);
			// setItems(search_items.data);
		// }
		// return;
	)
	if (isLoading) return 'Loading...'
	if (error) return 'An error occured: ' + error.message
	// useEffect(() => {
	// 	fetchItems(word);
	// }, [word])
	return (
		<div className='container'>
			<section className='section'>
				<div className='container'>
					<div className='row'>
						<div className='col-md-9'>
							<div className='row'>
								{/* <SearchContext.Provider value={{search_items, fetchItems}}> */}
									<>
										{
											search_items.map((search_item, index) => (
												<SearchResults key={index} word={search_item.word} lexicalCategory={search_item.lexicalCategory} translated_word={search_item.translated_word} definitions={search_item.definitions} pronunciations={search_item.pronunciations} synonyms={search_item.synonyms} antonyms={search_item.antonyms} homophones={search_item.homophones} examples={search_item.examples} online_examples={search_item.online_examples} search_id={search_item.search_id} vault_id={search_item.vault_id} />
											))
										}
									</>
								{/* </SearchContext.Provider> */}
							</div>
						</div>
						<div className='col-md-3'>
						</div>
					</div>
				</div>
			</section>
		</div>
	);
}

export default SearchHelper;
