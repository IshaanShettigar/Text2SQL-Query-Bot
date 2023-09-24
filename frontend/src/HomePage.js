import React from 'react';
import './HomePage.css'; // Import your CSS file

function HomePage() {
    return (
        <div>
            <header>
                <div className="lhs">
                    <div className="logo">
                        <img src={require("./assets/GEHCLOGO.png")} alt="LOGO" className="logo" />
                    </div>
                    <span>Product</span>
                    <span>About Us</span>
                </div>
                <div className="rhs">
                    <button className="try-now-btn">
                        <span>Try Now</span>
                        <i></i>
                    </button>
                </div>
            </header>

            <div className="hero-container">
                <div className="hero-text">
                    <h1>Unlock Your Data With Ease</h1>
                    <p>Introducing the Natural Language SQL Query Bot</p>
                    <button className="try-now-btn">Use Now for Free!</button>
                </div>
                <div className="hero-gif">
                    <img src={require("./assets/analyticsgif.gif")} alt="chat-gif" style={{ width: '700px' }} />
                </div>
            </div>
            <br />
            <hr style={{ width: '80%', margin: '0 auto', color: 'rgba(108, 108, 108, 0)' }} />
            <h1 style={{ width: '70%', fontSize: '35px', margin: '50px auto 50px auto' }}>
                Answer any question about your data in an instant
            </h1>
            <div className="info-container">
                <div className="info-gif">
                    <img src={require("./assets/infogif.gif")} alt="Informative GIF" style={{ width: '650px' }} />
                </div>
                <div className="info-text">
                    <h1>AI Powered Search in Natural Language</h1>
                    <p>
                        Our innovative solution simplifies database interactions like never before. With just plain language, you can
                        effortlessly request data and let our bot handle the complexity. Whether it's a straightforward query or a
                        complex database join involving multiple tables, our bot's got you covered. Say goodbye to technical jargon
                        and hello to effortless data retrieval!
                    </p>
                </div>
            </div>
            <div className="tech-super-container">
                <div className="tech-container">
                    <div className="tech-card">
                        <img className="icon" src={require("./assets/icons8-knowledge.png")} alt="Book icon" />
                        <p className="heading">External Knowledge</p>
                        <p className="body">
                            Through advanced technology, our AI acquires expertise in company-specific terminology. This enriches the AI's
                            language capabilities and broadens its comprehension, making it proficient in a wide range of topics while
                            accommodating the unique language of your business.
                        </p>
                    </div>
                    <div className="tech-card">
                        <img className="icon" src={require("./assets/icons8-data-protection.png")} alt="Unauthorized Icon" />
                        <p className="heading">Prevents Unauthorized Access</p>
                        <p className="body">
                            Our platform ensures that authorized users can maintain their accessibility while implementing robust
                            safeguards to thwart any attempts at malicious data requests, including preventing SQL injection attacks and
                            similar threats.
                        </p>
                    </div>
                    <div className="tech-card">
                        <img className="icon" src={require("./assets/icons8-data-privacy-64.png")} style={{ height: '50px' }} alt="Data Privacy icon" />
                        <p className="heading">Privacy</p>
                        <p className="body">
                            To ensure the utmost protection of your data, we have a strict policy of not transmitting your data to any
                            third-party AI services. All our AI products are self-hosted, reducing the risk of data leaks and maintaining
                            the highest level of data security.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default HomePage;
