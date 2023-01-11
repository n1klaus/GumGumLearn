import React, { useEffect, useState } from "react";
import NavDropdown from "react-bootstrap/NavDropdown";

const LanguageContext = React.createContext({
  languages: [],
  insertLanguageSvg: () => {},
});

const Languages = () => {
  const [languages, setLanguages] = useState([]);
  const fetchLanguages = async () => {
    const languages_response = await fetch(`http://localhost:8000/languages`);
    const language_items = await languages_response.json();
    // console.log(language_items.data)
    setLanguages(language_items.data);
  };
  const insertLanguageSvg = async (lang) => {
    const lang_svg = `${lang}_SVG`;
    console.log(lang_svg);
    return <lang_svg />;
  };
  useEffect(() => {
    fetchLanguages();
  });
  return (
    <LanguageContext.Provider value={{ languages, insertLanguageSvg }}>
      <>
        {languages.map((language, index) => (
          <NavDropdown.Item key={index} data-language-id={language.language_id}>
            {language.language_name}
            {insertLanguageSvg(language.language_name)}
          </NavDropdown.Item>
        ))}
      </>
    </LanguageContext.Provider>
  );
};

export default Languages;
