import {FormattedMessage} from 'react-intl';
import '../styles/Footer.css'

const Footer = () => (
        <footer className="footer">
            <p>
                <FormattedMessage id="project.app.Footer.text"/>
            </p>
        </footer>
);

export default Footer;