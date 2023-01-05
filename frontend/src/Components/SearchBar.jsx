import { ReactSearchAutocomplete } from 'react-search-autocomplete'
import { useState } from 'react';
import SearchHelper from '../SearchHelper';

export default function SearchBar() {
    const items = useState([]);

    const handleOnSearch = (string, results) => {
        // onSearch will have as the first callback parameter
        // the string searched and for the second the results.
        SearchHelper(string);
        console.log(string, results);
      }
    
      const handleOnHover = (result) => {
        // the item hovered
        console.log(result)
      }
    
      const handleOnSelect = (item) => {
        // the item selected
        console.log(item)
      }
    
      const handleOnFocus = () => {
        console.log('Focused')
      }
    
      const formatResult = (item) => {
        return (
          <>
            <span style={{ display: 'block', textAlign: 'left' }}>id: {item.id}</span>
            <span style={{ display: 'block', textAlign: 'left' }}>name: {item.name}</span>
          </>
        )
      }
    
	return (
		<div style={{ width: 400 }}>
          <ReactSearchAutocomplete
            items={items}
            onSearch={handleOnSearch}
            onHover={handleOnHover}
            onSelect={handleOnSelect}
            onFocus={handleOnFocus}
            // autoFocus
            formatResult={formatResult}
          />
        </div>
	)
}
