import {request} from './client';export const list=()=>request('/models');export const create=(body:unknown)=>request('/models','POST',body);
