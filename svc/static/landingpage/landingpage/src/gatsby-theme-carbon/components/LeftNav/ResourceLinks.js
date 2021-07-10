import React from 'react';
import ResourceLinks from 'gatsby-theme-carbon/src/components/LeftNav/ResourceLinks';

const links = [
  {
    title: 'gleam-playground',
    href: 'https://nicklas.xyz/apps/gleam-playground/',
  },
  // {
  //   title: 'Github',
  //   href: 'https://github.com/carbon-design-system/gatsby-theme-carbon',
  // },
  // {
  //   title: 'LinkedIn',
  //   href: 'https://www.carbondesignsystem.com',
  // },
  // {
  //   title: 'Configuration guide',
  //   href: '/guides/configuration',
  // },
];

// shouldOpenNewTabs: true if outbound links should open in a new tab
const CustomResources = () => <ResourceLinks shouldOpenNewTabs links={links} />;

export default CustomResources;
