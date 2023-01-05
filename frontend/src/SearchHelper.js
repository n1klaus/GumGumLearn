/* eslint-disable jsx-a11y/anchor-is-valid */
import React, {useEffect, useState} from "react";
import SearchResults from "./SearchResults";

const SearchContext = React.createContext({
	search_items: [],
	fetchItems: () => {}
})

export default function SearchHelper ({word}) {
	const [search_items, setItems] = useState([])
	
	const fetchItems = async (word) => {
		const items_response = await fetch(`http://localhost:8000/search?text=${word}`)
		const search_items = await items_response.json()
		// console.log(search_items.data)
		setItems(search_items.data)
	}
	useEffect(() => {
		fetchItems(word)
	})
	return (
		<div className='container'>
			<section className='section'>
				<div className='container'>
					<div className='row'>
						<div className='col-md-9'>
							<div className='row'>
								<SearchContext.Provider value={{search_items, fetchItems}}>
									<>
										{
											search_items.map((search_item, index) => (
												<SearchResults key={index} word={search_item.word} translated_word={search_item.translated_word} definitions={search_item.definitions} pronunciations={search_item.pronunciations} synonyms={search_item.synonyms} antonyms={search_item.antonyms} homophones={search_item.homophones} examples={search_item.examples} online_examples={search_item.online_examples} search_id={search_item.search_id} vault_id={search_item.vault_id} fetchItems={fetchItems} />
											))
										}
									</>
								</SearchContext.Provider>
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
