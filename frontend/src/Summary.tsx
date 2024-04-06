const Summary = () => {
  return (
    <div className="flex flex-col h-full items-center space-y-8">
      <video className="h-full w-full rounded-lg" controls>
        <source src="/final_with_ai_voice.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>

      <p className="text-2xl">
        Barcelona and Paris Saint-Germain are facing each other in the last 16
        of the Champions League. The match has an incredible atmosphere with
        fans cheering on the players. Both teams are giving their all on the
        field, with Messi, Neymar, and Cavani showcasing their skills. The game
        ends with Barcelona winning 6-1, securing their spot in the next round.
        The victory is historic and may not be seen again, showing the talent
        and determination of the players. It was a thrilling match filled with
        goals, penalties, and fantastic plays.
      </p>
    </div>
  );
};

export default Summary;
