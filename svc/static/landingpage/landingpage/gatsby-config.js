module.exports = {
    siteMetadata: {
        title: "Nicklas Sindlev Andersen",
        description: "A personal blog & portfolio website belonging to Nicklas Sindlev Andersen",
        keywords: "portfolio,programming,code,blog,lab",
    },
    plugins: [
        {
            resolve: "gatsby-plugin-manifest",
            options: {
                navigationStyle: "header",
                name: "Carbon Design Gatsby Theme",
                icon: "src/images/favicon.svg",
                short_name: "Gatsby Theme Carbon",
                start_url: "/",
                background_color: "#ffffff",
                theme_color: "#0062ff",
                display: "browser",
            },
        },
        {
            resolve: "gatsby-theme-carbon",
            options: {
                theme: {
                    homepage: "dark",
                    interior: "dark",
                },
            },
        },
    ],
};
