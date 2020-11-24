export const PRODUCTION = 'PRODUCTION'
export const STAGING = 'STAGING'
export const DEVELOPMENT = 'DEVELOPMENT'

const IKEM = {
  'primary-color': '#e2001a',
  'logo-background-image': 'url("../../../assets/img/logo_ikem.svg")',
  'logo-background-size': '94px 70px',
  'logo-width': '100px',
  'logo-height': '70px'
}

export const THEMES = {
  [PRODUCTION]: IKEM,
  [STAGING]: {
    'primary-color': '#2D4496',
    'logo-background-image': 'url("../../../assets/img/logo_mild_blue.svg")',
    'logo-background-size': '160px 60px',
    'logo-width': '170px',
    'logo-height': '70px'
  },
  [DEVELOPMENT]: IKEM
}
