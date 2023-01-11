import React from "react";
import { SocialIcon } from "react-social-icons";

const Footer = () => {
  return (
    <div className="footer-container mt-3">
      <div className="mb-3">
        <SocialIcon url="https://twitter.com/#" />
        <SocialIcon url="https://github.com/#" />
        <SocialIcon url="https://discord.com/#" />
        <SocialIcon url="https://telegram.com/#" />
        <SocialIcon url="https://whatsapp.com/#" />
      </div>
      <div className="mb-3 w-100">
        <div className="row text-center">
          <div className="col-lg-6">
            <p className="copyright mb-0 ">
              {" "}
              Copyright &copy; 2023 <a href="/home">GumGumLearn &trade;</a>
            </p>
          </div>
          <div className="col-lg-6">
            <ul className="list-inline mb-0 footer-btm-links text-lg-right mt-2 mt-lg-0">
              <li className="list-inline-item">
                <a href="/privacy">Privacy Policy</a>
              </li>
              <li className="list-inline-item">
                <a href="/terms">Terms &amp; Conditions</a>
              </li>
              <li className="list-inline-item">
                <a href="/cookies">Cookie Policy</a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};
export default Footer;
