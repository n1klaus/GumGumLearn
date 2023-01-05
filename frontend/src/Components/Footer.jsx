import React from "react";
import { SocialIcon } from 'react-social-icons';

const Header = () => {
	return (
		<div className='footer-btm py-4 '>
				<div className='flex'>
									<SocialIcon url="https://twitter.com/#" />
									<SocialIcon url="https://facebook.com/#" />
									<SocialIcon url="https://instagram.com/#" />
									<SocialIcon url="https://discord.com/#" />
									<SocialIcon url="https://telegram.com/#" />
								</div>
				<div className='container'>
					<div className='row text-center'>
						<div className='col-lg-6'>
							<p className='copyright mb-0 '> Copyright &copy; 2022 <a href='/home'>GumGumLearn &trade;</a></p>
						</div>
						<div className='col-lg-6'>
							<ul className='list-inline mb-0 footer-btm-links text-lg-right mt-2 mt-lg-0'>
								<li className='list-inline-item'><a href='/privacy'>Privacy Policy</a></li>
								<li className='list-inline-item'><a href='/termsandconditions'>Terms &amp; Conditions</a></li>
								<li className='list-inline-item'><a href='/cookies'>Cookie Policy</a></li>
								<li className='list-inline-item'><a href='/contracts'>Terms of Sale</a></li>
							</ul>
						</div>
					</div>
				</div>
			</div>
	);
};
export default Header