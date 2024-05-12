<template>
<table class="table">
  <thead>
    <tr>
      <th scope="col">ID</th>
      <th scope="col">Song</th>
      <th scope="col">Author</th>
      <th scope="col">Action</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="music in musicList">
        <td>{{ music.id }}</td>
        <td>{{ music.title }}</td>
        <td>{{ music.author }}</td>
        <td>Play</td>
    </tr>
  </tbody>
</table>    
</template>

<script>
import { mapState } from 'pinia';
import { useCommonStore } from '../stores/common';
import Music from '@/lib/music';

export default {
  name: 'MusicList',
  mounted(){
    this.loadMusic();
  },
  data(){
    return {
        musicList: [],
    };
  },
  methods:{
    async loadMusic(){
        console.log(this.apiUrl);
        const musicList = await Music.loadAllMusic(this.apiUrl);
        this.musicList = musicList;
    },
  },
  computed: {
    ...mapState(useCommonStore, ['apiUrl'])
  },
}
</script>

<style scoped lang="scss">

</style>