<script setup lang="ts">defineProps<{rows:string[]}>()</script><template><aside v-if="rows.length" class="warning-notes"><p v-for="(r,i) in rows" :key="i">{{r}}</p></aside></template>
