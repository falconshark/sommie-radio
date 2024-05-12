<template>
    <div class="music-player-wrapper">
        Currently Playing:
        <div class="music-player">
            <figure>
                <audio controls :src="musicUrl"></audio>
            </figure>
        </div>
    </div>
</template>

<script>
import { mapState } from 'pinia';
import { useCommonStore } from '../stores/common';
export default {
  name: 'MusicPlayer',
  mounted(){
    this.loadMusic();
  },
  data(){
    return {
        musicUrl: '',
    }
  },
  methods:{
    loadMusic(){
        this.musicUrl = `${this.apiUrl}/streaming`;
    },
  },
  computed: {
    ...mapState(useCommonStore, ['apiUrl'])
  },
}
</script>

<style lang="scss">
.music-player{
    margin-top: 10px;
}
</style>