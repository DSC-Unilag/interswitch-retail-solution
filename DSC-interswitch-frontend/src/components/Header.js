import React from "react";
import "./css/Header.css";

class Header extends React.Component {
	render() {
		return (
			<div>
				<div className='container header'>
					<div className='row'>
						<div className='col-md-6 d-flex justify-content-center align-items-center'>
							<form className='form-inline'>
								<div className='form-group mr-1'>
									<input
										className='form-control'
										type='text'
									/>
								</div>
								<div className='form-group'>
									<input
										className='btn btn-primary'
										type='submit'
										value='Search'
									/>
								</div>
							</form>
						</div>
						<div className='col-md-6 d-flex justify-content-center align-items-center'>
							{/* <img
								src='./Images/man.svg'
								alt='Logo'
								className='mr-4'
                            /> */}
							<p>
								<img alt='Logo' src='./Images/man.svg' />
							</p>
							<h3>Login</h3>
						</div>
					</div>
				</div>
			</div>
		);
	}
}

export default Header;
