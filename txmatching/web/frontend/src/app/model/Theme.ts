export const ikem = 'IKEM';
export const mild_blue = 'MILD_BLUE';

interface ThemeDefinition {
  [key: string]: string;
}

interface ThemesType {
  [key: string]: ThemeDefinition;
}

const IKEMTheme: ThemeDefinition = {
  'primary-color': '#e2001a',
  'logo-background-image': 'url("../../../assets/img/logo_ikem.svg")',
  'logo-background-size': 'contain',
  'logo-width': '57px',
  'logo-height': '50px',
  'favicon-ico': 'assets/img/favicons_ikem/favicon.ico',
  'favicon-16x16': 'assets/img/favicons_ikem/favicon-16x16.png',
  'favicon-32x32': 'assets/img/favicons_ikem/favicon-32x32.png',
  'apple-touch-icon': 'assets/img/favicons_ikem/apple-touch-icon.png'
};


const MildBlueTheme: ThemeDefinition = {
  'primary-color': '#2D4496',
  'logo-background-image': 'url("../../../assets/img/logo_mild_blue.svg")',
  'logo-background-size': 'contain',
  'logo-width': '101px',
  'logo-height': '36px',
  'favicon-ico': 'assets/img/favicons_mildblue/favicon.ico',
  'favicon-16x16': 'assets/img/favicons_mildblue/favicon-16x16.png',
  'favicon-32x32': 'assets/img/favicons_mildblue/favicon-32x32.png',
  'apple-touch-icon': 'assets/img/favicons_mildblue/apple-touch-icon.png'
};

export const theme: ThemesType = {
  IKEM: IKEMTheme,
  MILD_BLUE: MildBlueTheme,
};
