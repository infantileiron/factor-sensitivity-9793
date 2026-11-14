import {request} from './client';export const list=()=>request('/spaces');export const create=(body:unknown)=>request('/spaces','POST',body);
