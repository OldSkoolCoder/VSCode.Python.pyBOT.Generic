var socialsCollectionIndex = 0;
var twisCollectionIndex = 1;
var socialImageBkColour = "backgroundBlack";
var socialsInformationArray = []

function initialiseBanner()
{
    SocialDivImage = document.getElementById('divImgSocial');
    SocialImage = document.getElementById('imgSocial');
    SocialInformation = document.getElementById('socialInfo');

    // console.log(socialsInformationArray);

    // console.log(socialsCollectionIndex);

    // console.log(socialsInformationArray[socialsCollectionIndex]);

    // SocialDivImage.classList.remove(SocialDivImage.classList.contains('background'));
    SocialDivImage.classList.remove(socialImageBkColour);
    SocialImage.src = "Assets\\" + socialsInformationArray[socialsCollectionIndex].image + ".png";
    SocialInformation.innerHTML = socialsInformationArray[socialsCollectionIndex].info
    socialImageBkColour = "background" + socialsInformationArray[socialsCollectionIndex].imageBackColour;
    SocialDivImage.classList.add(socialImageBkColour);
}

function moveSocialBanner()
{
    SocialContainer = document.getElementById('socialCollection');
    SocialContainer.style.left = 0;

    // console.log(SocialContainerCount, socialsCollectionIndex);

    setTimeout(() => {
        SocialContainer.style.left = 450;
        socialsCollectionIndex++;
        // console.log(SocialContainerCount, socialsCollectionIndex);
        if (socialsCollectionIndex == socialsInformationArray.length)
        {
            socialsCollectionIndex = 0;
        }

        setTimeout(() => {
            initialiseBanner();
            moveSocialBanner();
        }, 3000);
    }, 14000)
}

function moveTwitchInformationBanners()
{
    twiContainer = document.getElementById('TwitchInformation');
    twiContainerCount = twiContainer.childNodes.length;
    twiBanner = twiContainer.childNodes[twisCollectionIndex];
    twiBanner.style.left = 10;

    // console.log(twiContainerCount, twisCollectionIndex);

    setTimeout(() => {
        twiBanner.style.left = -1200;
        twisCollectionIndex = twisCollectionIndex + 2;
        console.log(twiContainerCount, twisCollectionIndex);
        if (twisCollectionIndex == twiContainerCount)
        {
            twisCollectionIndex = 1;
        }

        setTimeout(() => {
            moveTwitchInformationBanners();
        }, 3000);
    }, 30000)
}

function loadSocialsJSON()
{
    fetch('JSON/socials.json')
    .then((response) => response.json())
    .then((json) => {
        //console.log(json);
        json.socials.forEach(element => {
            socialsInformationArray.push(element)
        });
        // console.log(socialsInformationArray);
        initialiseBanner();
        }
    );    
}