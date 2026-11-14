import {request} from './client';export const list=()=>request('/studies');export const create=(body:unknown)=>request('/studies','POST',body);
