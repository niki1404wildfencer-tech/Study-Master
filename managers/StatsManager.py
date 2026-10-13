import pandas as pd
import numpy as np


class StatisticsManager:

    def __init__(self):
        self.session_df = pd.DataFrame()

        # Daily goal is supplied by TimerPage / StatsPage.
        # Default is 0 until the user sets one.
        self.daily_goal_minutes = 0

    # =========================================================
    # SESSION DATA
    # =========================================================

    def set_sessions(self, sessions):
        """
        Receive sessions from SessionManager and convert them
        into a Pandas DataFrame.
        """

        if not sessions:
            self.session_df = pd.DataFrame()
            return

        self.session_df = pd.DataFrame(sessions)

        self.prepare_data()

    def prepare_data(self):
        """
        Clean and prepare the session DataFrame.

        Gregorian dates are kept internally.
        Jalali conversion belongs to the UI/display layer.
        """

        if self.session_df.empty:
            return

        df = self.session_df

        # -----------------------------------------------------
        # Make sure required columns exist
        # -----------------------------------------------------

        required_columns = [
            "id",
            "subject_id",
            "task_id",
            "planned_duration",
            "actual_duration",
            "started_at",
            "finished_at",
            "date",
            "status",
        ]

        for column in required_columns:

            if column not in df.columns:
                df[column] = None

        # -----------------------------------------------------
        # Date
        # -----------------------------------------------------

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce",
        )

        # -----------------------------------------------------
        # Duration
        # -----------------------------------------------------

        df["planned_duration"] = pd.to_numeric(
            df["planned_duration"],
            errors="coerce",
        ).fillna(0)

        df["actual_duration"] = pd.to_numeric(
            df["actual_duration"],
            errors="coerce",
        ).fillna(0)

        # -----------------------------------------------------
        # Remove invalid dates
        # -----------------------------------------------------

        df.dropna(
            subset=["date"],
            inplace=True,
        )

        self.session_df = df

    # =========================================================
    # DAILY STUDY
    # =========================================================

    def get_daily_study(self):
        """
        Return total study time for every day.

        Result:

            date | actual_duration
        """

        if self.session_df.empty:
            return pd.DataFrame(
                columns=[
                    "date",
                    "actual_duration",
                ]
            )

        return (
            self.session_df
            .groupby("date", as_index=False)
            ["actual_duration"]
            .sum()
            .sort_values("date")
        )

    # =========================================================
    # WEEKLY STUDY
    # =========================================================

    def get_weekly_study(self):
        """
        Return study data for the last 7 days.

        Data is grouped by:

            date
            subject_id

        This allows the chart to later use different colors
        for different subjects.
        """

        if self.session_df.empty:
            return pd.DataFrame(
                columns=[
                    "date",
                    "subject_id",
                    "actual_duration",
                ]
            )

        today = pd.Timestamp.today().normalize()

        start_date = (
            today - pd.Timedelta(days=6)
        )

        df = self.session_df[
            (self.session_df["date"] >= start_date)
            &
            (self.session_df["date"] <= today)
        ]

        return (
            df
            .groupby(
                [
                    "date",
                    "subject_id",
                ],
                as_index=False,
            )
            ["actual_duration"]
            .sum()
            .sort_values("date")
        )

    # =========================================================
    # MONTHLY STUDY
    # =========================================================

    def get_monthly_study(self):
        """
        Return study data from the beginning of the
        current calendar month until today.

        No assumption is made about the number of days
        in a month.
        """

        if self.session_df.empty:
            return pd.DataFrame(
                columns=[
                    "date",
                    "subject_id",
                    "actual_duration",
                ]
            )

        today = pd.Timestamp.today().normalize()

        start_date = today.replace(
            day=1
        )

        df = self.session_df[
            (self.session_df["date"] >= start_date)
            &
            (self.session_df["date"] <= today)
        ]

        return (
            df
            .groupby(
                [
                    "date",
                    "subject_id",
                ],
                as_index=False,
            )
            ["actual_duration"]
            .sum()
            .sort_values("date")
        )
    def get_yearly_study(self):
        """۱۲ ماه اخیر، تجمیع ماهانه"""
        if self.session_df.empty:
            return pd.DataFrame(
                columns=["date", "subject_id", "actual_duration"]
            )

        today = pd.Timestamp.today().normalize()
        start_date = today - pd.Timedelta(days=364)

        df = self.session_df[
            (self.session_df["date"] >= start_date) &
            (self.session_df["date"] <= today)
        ].copy()

        if df.empty:
            return pd.DataFrame(
                columns=["date", "subject_id", "actual_duration"]
            )

        df["subject_id"] = df["subject_id"].fillna(-1).astype(int)
        df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

        result = (
            df.groupby(["month", "subject_id"], as_index=False)
            ["actual_duration"]
            .sum()
        )
        result = result.rename(columns={"month": "date"})
        return result.sort_values("date")


    def get_all_time_study(self):
        """همه سشنها، تجمیع ماهانه"""
        if self.session_df.empty:
            return pd.DataFrame(
                columns=["date", "subject_id", "actual_duration"]
            )

        df = self.session_df.copy()
        df["subject_id"] = df["subject_id"].fillna(-1).astype(int)
        df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

        result = (
            df.groupby(["month", "subject_id"], as_index=False)
            ["actual_duration"]
            .sum()
        )
        result = result.rename(columns={"month": "date"})
        return result.sort_values("date")
        # =========================================================
        # STUDY TIME BY SUBJECT
        # =========================================================

    def get_study_time_by_subject(self):
        """
        Return total study time grouped by subject.
        """

        if self.session_df.empty:
            return pd.Series(
                dtype="float64"
            )

        return (
            self.session_df
            .groupby("subject_id")
            ["actual_duration"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

    # =========================================================
    # STUDY TIME BY SUBJECT - DATAFRAME
    # =========================================================

    def get_study_time_by_subject_df(self):
        """
        Same information as get_study_time_by_subject(),
        but returned as a DataFrame.

        Useful for Matplotlib.
        """

        if self.session_df.empty:
            return pd.DataFrame(
                columns=[
                    "subject_id",
                    "actual_duration",
                ]
            )

        return (
            self.session_df
            .groupby(
                "subject_id",
                as_index=False,
            )
            ["actual_duration"]
            .sum()
            .sort_values(
                "actual_duration",
                ascending=False,
            )
        )

    # =========================================================
    # AVERAGE SESSION
    # =========================================================

    def get_average_session_duration(self):
        """
        Return average completed study-session duration.
        """

        if self.session_df.empty:
            return 0.0

        durations = (
            self.session_df[
                self.session_df["actual_duration"] > 0
            ]["actual_duration"]
            .to_numpy()
        )

        if len(durations) == 0:
            return 0.0

        return float(
            np.mean(durations)
        )

    # =========================================================
    # TOTAL STUDY TIME
    # =========================================================

    def get_total_study_minutes(self):
        """
        Return total study time across all sessions.
        """

        if self.session_df.empty:
            return 0.0

        durations = (
            self.session_df["actual_duration"]
            .to_numpy()
        )

        return float(
            np.sum(durations)
        )

    # =========================================================
    # MOST STUDIED SUBJECT
    # =========================================================

    def get_most_studied_subject(self):
        """
        Return the subject with the highest total study time.

        Returns:
            subject_id
            or None when there is no data.
        """

        study_by_subject = (
            self.get_study_time_by_subject()
        )

        if study_by_subject.empty:
            return None

        return study_by_subject.index[0]

    # =========================================================
    # MOST STUDIED SUBJECT DATA
    # =========================================================

    def get_most_studied_subject_data(self):
        """
        Return both subject and study time.
        """

        study_by_subject = (
            self.get_study_time_by_subject()
        )

        if study_by_subject.empty:
            return None

        subject_id = (
            study_by_subject.index[0]
        )

        minutes = float(
            study_by_subject.iloc[0]
        )

        return {
            "subject_id": subject_id,
            "minutes": minutes,
        }

    # =========================================================
    # DAILY GOAL
    # =========================================================

    def set_daily_goal(self, minutes):
            """
            Set the user's daily study goal.
            """

            try:
                minutes = float(minutes)
            except (
                TypeError,
                ValueError,
            ):
                return

            if minutes < 0:
                return

            self.daily_goal_minutes = minutes

    def get_daily_goal(self):
            """
            Return current daily goal.
            """

            return self.daily_goal_minutes

        # =========================================================
        # TODAY'S STUDY
        # =========================================================

    def get_today_study_minutes(self):
        """
        Return today's total study time.
        """

        if self.session_df.empty:
            return 0.0

        today = (
            pd.Timestamp.today()
            .normalize()
        )

        today_data = self.session_df[
            self.session_df["date"] == today
        ]

        if today_data.empty:
            return 0.0

        return float(
            today_data["actual_duration"]
            .sum()
        )
    # In StatsManager.py, add after get_today_study_minutes:

    def get_today_study_by_subject(self):

        if self.session_df.empty:

            return {}

        today = (
             pd.Timestamp.today()
            .normalize()
            )

        today_data = self.session_df[
            self.session_df["date"] == today
            ]

        if today_data.empty:

            return {}

        grouped = (
            today_data
            .groupby("subject_id")[
                "actual_duration"
            ]
            .sum()
        )

        result = {}

        for subject_id, minutes in grouped.items():

            try:

                subject_id = int(subject_id)

            except (
                TypeError,
                ValueError,
            ):

                continue

            result[subject_id] = float(
                minutes
            )

        return result
    # =========================================================
    # DAILY GOAL PROGRESS
    # =========================================================

    def get_daily_goal_progress(
        self,
        daily_goal_minutes=None,
    ):
        """
        Return today's progress as a value
        between 0 and 1.

        Example:

            goal = 120 minutes
            studied = 60 minutes

            result = 0.5
        """

        if daily_goal_minutes is None:
            daily_goal_minutes = (
                self.daily_goal_minutes
            )

        try:
            daily_goal_minutes = float(
                daily_goal_minutes
            )
        except (
            TypeError,
            ValueError,
        ):
            return 0.0

        if daily_goal_minutes <= 0:
            return 0.0

        today_study = (
            self.get_today_study_minutes()
        )

        progress = (
            today_study /
            daily_goal_minutes
        )

        return float(
            np.clip(
                progress,
                0.0,
                1.0,
            )
        )

    # =========================================================
    # DAILY GOAL INFORMATION
    # =========================================================

    def get_daily_goal_data(self):
        """
        Return everything needed by the Daily Goal card.
        """

        goal = float(
            self.daily_goal_minutes
        )

        studied = (
            self.get_today_study_minutes()
        )

        progress = (
            self.get_daily_goal_progress()
        )

        return {
            "goal_minutes": goal,
            "studied_minutes": studied,
            "progress": progress,
            "percentage": progress * 100,
            "completed": (
                studied >= goal
                if goal > 0
                else False
            ),
        }

    # =========================================================
    # WEEKLY TOTAL
    # =========================================================

    def get_weekly_total_minutes(self):
        """
        Return total study time for the last 7 days.
        """

        data = (
            self.get_weekly_study()
        )

        if data.empty:
            return 0.0

        return float(
            data["actual_duration"]
            .sum()
        )

    # =========================================================
    # MONTHLY TOTAL
    # =========================================================

    def get_monthly_total_minutes(self):
        """
        Return total study time for the current month.
        """

        data = (
            self.get_monthly_study()
        )

        if data.empty:
            return 0.0

        return float(
            data["actual_duration"]
            .sum()
        )

    # =========================================================
    # DAILY TREND - TOTAL
    # =========================================================

    def get_daily_trend(self, period="Weekly"):
        """
        Return one total value for every day.

        This is the easiest format for a simple bar chart.
        """

        if period == "Monthly":
            data = (
                self.get_monthly_study()
            )
        else:
            data = (
                self.get_weekly_study()
            )

        if data.empty:
            return pd.DataFrame(
                columns=[
                    "date",
                    "actual_duration",
                ]
            )

        return (
            data
            .groupby(
                "date",
                as_index=False,
            )
            ["actual_duration"]
            .sum()
            .sort_values("date")
        )

    # =========================================================
    # DAILY TREND - SUBJECT BREAKDOWN
    # =========================================================

    def get_daily_trend_by_subject(self, period="Weekly"):
        if period == "Monthly":
            return self.get_monthly_study()
        if period == "Yearly":
            return self.get_yearly_study()
        if period == "All Time":
            return self.get_all_time_study()
        return self.get_weekly_study()
    # =========================================================
    # SUMMARY
    # =========================================================

    def get_summary(self):
        """
        Return the main statistics required by StatsPage.
        """

        most_studied = (
            self.get_most_studied_subject_data()
        )

        goal_data = (
            self.get_daily_goal_data()
        )

        return {
            "today_minutes":
                self.get_today_study_minutes(),

            "weekly_minutes":
                self.get_weekly_total_minutes(),

            "monthly_minutes":
                self.get_monthly_total_minutes(),

            "average_session_minutes":
                self.get_average_session_duration(),

            "most_studied_subject":
                (
                    most_studied["subject_id"]
                    if most_studied
                    else None
                ),

            "most_studied_subject_minutes":
                (
                    most_studied["minutes"]
                    if most_studied
                    else 0.0
                ),

            "daily_goal_minutes":
                goal_data["goal_minutes"],

            "daily_goal_studied_minutes":
                goal_data["studied_minutes"],

            "daily_goal_progress":
                goal_data["progress"],

            "daily_goal_percentage":
                goal_data["percentage"],
        }

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self):
        """
        Clear loaded statistics data.
        """

        self.session_df = pd.DataFrame()