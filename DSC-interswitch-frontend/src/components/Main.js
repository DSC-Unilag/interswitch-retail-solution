import React, { Component } from "react";
import "./css/Main.css";

export default class Main extends Component {
	render() {
		return (
			<div>
				<div className='container' style={{ marginTop: "3em" }}>
					<div className='row'>
						<div className='col-md-8 d-flex align-items-center mb-4'>
							<div className='jumbotrom' style={{}}>
								<h3 style={{ color: "grey" }}>
									Bridging the gap between
									<span
										style={{
											color: "#073954",
											margin: "0px 3px"
										}}
									>
										Consumers
									</span>
									<br /> and
									<span
										style={{
											color: "#169fe9",
											padding: "0px 3px"
										}}
									>
										Manufacturers
									</span>
								</h3>
								<div className='row'>
									<p
										className='mr-4'
										style={{
											background: "#073954",
											color: "#fff",
											padding: "4px 10px",
											borderRadius: "5px",
											// fontWeight: "bold",
											marginLeft: "1rem"
										}}
									>
										Get Supplies
									</p>
									<p
										style={{
											background: "#169fe9",
											color: "#fff",
											padding: "4px 30px",
											borderRadius: "5px"
											// fontWeight: "bold"
										}}
									>
										Supply
									</p>
								</div>
							</div>
						</div>
						<div
							className='col-md-4 pt-4'
							style={{ background: "#eee" }}
						>
							<h3>Categories</h3>
							<p>Groceries</p>
							<p>Provisions</p>
							<p>Groceries</p>
							<p>Provisions</p>
							<p>Groceries</p>
							<p>Provisions</p>
							<p>Groceries</p>
						</div>
					</div>
				</div>
			</div>
		);
	}
}
