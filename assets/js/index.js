import '../scss/main.scss';
import {v4 as uuidv4} from 'uuid';
import * as utils from "./common.js";

window.uuidv4 = uuidv4;
window.utils = utils;
