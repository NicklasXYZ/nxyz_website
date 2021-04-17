import React from "react";
import { HomepageBanner, HomepageCallout } from "gatsby-theme-carbon";
import HomepageTemplate from "./HomepageTemplate";
import { calloutLink } from "./Homepage.module.scss";


const FirstLeftText = () => <p style={{fontSize:"1.5rem"}}>Who Am I?</p>;

const FirstRightText = () => (
    <p style={{fontSize:"1.5rem"}}>
    I am a PhD student in computer science and a part of the 
    {' '}<a href="https://dss.sdu.dk/">Data Science and Statistics</a> (DSS)
    group at the <a href="https://www.sdu.dk/en/">University of Southern Denmark</a> (SDU).
    My research interests are in the area of data science and software engineering:
        <ul>
            <li> - Data analysis & visualization</li>
            <li> - AI for decision making</li>
            <li> - Linear & non-linear optimization</li>
            <li> - Distributed systems </li>
        </ul> 
    </p>
);

const BannerText = () => <h1>Nicklas Sindlev Andersen</h1>;

const customProps = {
    Banner: (
    <>
    <span className="homepage--dots" />
        <section className="homepage--header">
            <HomepageBanner renderText={BannerText} image={null}/>,
        </section>
    </>
    ),
    FirstCallout: (
        <HomepageCallout
        backgroundColor="#030303"
        color="white"
        leftText={FirstLeftText}
        rightText={FirstRightText}
        />
    ),
};

// spreading the original props gives us props.children (mdx content)
function ShadowedHomepage(props) {
    return <HomepageTemplate {...props} {...customProps} />;
}

export default ShadowedHomepage;
