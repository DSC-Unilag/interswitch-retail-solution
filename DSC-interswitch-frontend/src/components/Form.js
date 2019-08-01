import React from "react";

class Form extends React.Component {
	render() {
		return (
			<div>
				<div className='container' style={{ marginTop: "4em" }}>
					<div className='row'>
						<div className='col-md-6 pt-4'>
							<h3 className='mb-4' style={{ color: "#169fe9" }}>
								Consumer
								<span style={{ fontWeight: "bold" }}>
									Manufacturer
								</span>
							</h3>
							<form>
								<div className='form-group'>
									<input
										type='text'
										class='form-control'
										placeholder='Email address'
									/>
								</div>
								<div className='form-group'>
									<input
										type='text'
										class='form-control'
										placeholder='Email address'
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
						<div className='col-md-6' />
					</div>
				</div>
			</div>
		);
	}
}

export default Form;
