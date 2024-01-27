import React from 'react';
import { Navbar, Nav, NavDropdown } from 'react-bootstrap';
import logo from './logo.png';  // replace 'logo.png' with your logo file name


<Navbar.Brand href="#home">
    <img
        alt="Logo"
        src={logo}
        width="30"
        height="30"
        className="d-inline-block align-top"
    />
</Navbar.Brand>


const NavigationBar = () => {
    return (
        <Navbar bg="light" expand="lg">
            <Navbar.Brand href="#home">Logo</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">
                    <Nav.Link href="#home">Home</Nav.Link>
                    <Nav.Link href="#login">Log-in</Nav.Link>
                    <Nav.Link href="#about">About Us</Nav.Link>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    );
};

export default NavigationBar;


