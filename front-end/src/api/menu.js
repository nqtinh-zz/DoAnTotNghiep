const Menu = [
  // { header: '' },
  {
    title: 'F.Smart Door',
    value: 'FSmartDoor',
    icon: 'people',
    link: '/fsmartdoor'
  },
  {
    title: 'Fire Detect',
    value: 'FireDetect',
    icon: 'location_on',
    link: '/firedetect'
  },
  {
    title: 'People Couting',
    value: 'PeopleCouting',
    icon: 'camera',
    link: '/peoplecouting'
  },
  {
    title: 'View Statistics',
    value: 'viewStatistic',
    icon: 'list',
    link: '/viewstatistic'
  }
]
// reorder menu
Menu.forEach((item) => {
  if (item.blocks) {
    item.blocks.sort((x, y) => {
      let textA = x.title.toUpperCase()
      let textB = y.title.toUpperCase()
      return (textA < textB) ? -1 : (textA > textB) ? 1 : 0
    })
  }
})

export default Menu
