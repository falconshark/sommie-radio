import queryString from 'query-string';

const Music = {
    async loadAllMusic(baseApiUrl) {
        const apiUrl = `${baseApiUrl}/music`;
        const fetchResult = await fetch(apiUrl);
        const status = await fetchResult.status;

        //If cannot connect with API server
        if (status !== 200 && status !== 401) {
            const err = 'Cannot loading music information. Maybe there are some network problem?';
            return err;
        }
        const resultJson = await fetchResult.json();
        return resultJson;
    },
}

export default Music;