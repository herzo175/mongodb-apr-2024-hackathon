const Summary = () => {
  return (
    <div className="flex flex-col h-full items-center space-y-8">
      <video className="h-full w-full rounded-lg" controls>
        <source src="/messi-summary.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>

      <p className="text-2xl">
        The speaker describes a football match where one team scores three
        goals. The commentator is impressed by a special goal from Messi that
        catches the goalkeeper off guard. The commentator emphasizes how
        difficult it was to beat the goalkeeper from that distance and praises
        Messi's skill in scoring the goal.
      </p>
    </div>
  );
};

export default Summary;
