import NavDropdown from "react-bootstrap/NavDropdown";
import { useState } from "react";

const Languages = () => {
  const [lang_title, setTitle] = useState("");
  const setLanguage = (val) => {
    document.getElementById("dropdown-menu").innerText = val;
    setTitle(val);
  };
  return (
    <>
      <NavDropdown
        title="Language"
        id={"dropdown-menu"}
        data-language={lang_title}
      >
        <NavDropdown.Item onClick={(e) => setLanguage(e.target.innerText)}>
          EN-GB
        </NavDropdown.Item>
        <NavDropdown.Item onClick={(e) => setLanguage(e.target.innerText)}>
          En-US
        </NavDropdown.Item>
      </NavDropdown>
    </>
  );
};

export default Languages;
